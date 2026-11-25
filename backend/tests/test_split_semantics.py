import json
import pytest
from app.services.split_semantics import Pipeline,classification_input,LocalModel,composition_complete
from app.services.semantic_errors import SemanticError

class Client:
    def __init__(self):self.calls=[]
    def model_digest(self,model):return model+'-digest'
    def infer(self,model,prompt,data,output_schema):
        self.calls.append((model,data))
        if 'title' in data:return {'name_ko':'피규어'},{'seconds':1}
        return {'franchise':None,'characters':[],'figure_form':None},{'seconds':1}

@pytest.mark.parametrize('url',['https://api.openai.com','http://example.com','http://user:secret@localhost:11434','http://localhost:11434/remote'])
def test_split_pipeline_rejects_remote_or_credentialed_endpoint(url):
    with pytest.raises(SemanticError,match='LOCAL_OLLAMA_ENDPOINT_REQUIRED'):LocalModel(url)

def test_dictionary_composition_does_not_publish_untranslated_english_words():
    assert not composition_complete('피규어 REBOOT')
    assert composition_complete('미라지 C02-URANUS 1/7 PVC')

def source():
    return {'name_original':'謎のフィギュア','official_url':'https://example.com/item/1','manufacturer':'TAITO','type':'figure'}

def pipeline(tmp_path,client=None):return Pipeline({'fingerprint':'test','titles':{}},client or Client(),tmp_path)

def test_long_description_is_not_sent_to_translation_and_stages_resume(tmp_path):
    client=Client();p=pipeline(tmp_path,client);s={**source(),'document_0':'x'*100000}
    first=p.translate(s);again=p.translate(s)
    assert again['cache_hit'] and len(client.calls)==1
    assert 'document_0' not in client.calls[0][1]
    p.classify(s,first);p.classify(s,first)
    assert len(client.calls)==2 and client.calls[1][0]=='qwen3:1.7b'
    assert len(client.calls[1][1]['original_fields']['document_0'])<=240

def test_invalid_translation_is_not_cached(tmp_path):
    class Bad(Client):
        def infer(self,*args):return {'name_ko':'謎のフィギュア'},{'seconds':1}
    p=pipeline(tmp_path,Bad())
    with pytest.raises(SemanticError,match='TRANSLATION_VALIDATION_FAILED'):p.translate(source())
    assert not list(tmp_path.glob('translation_*.json'))

def test_failed_simple_translation_uses_covered_parts_and_review(tmp_path):
    class Recovery(Client):
        def infer(self,model,prompt,data,output_schema):
            self.calls.append((model,data))
            if 'parts' in output_schema['properties']:
                return {'parts':[{'source':data['title'],'ko':'수수께끼의 피규어'}]},{'seconds':2}
            if 'approved' in output_schema['properties']:
                return {'approved':True,'issues':[]},{'seconds':1}
            return {'name_ko':'謎のフィギュア'},{'seconds':1}
    c=Recovery();p=pipeline(tmp_path,c);r=p.translate(source())
    assert r['method']=='translation_parts_review' and r['seconds']==4
    # initial + glossary (invalid here, so ignored) + parts + review
    assert len(c.calls)==4
    p.translate(source());assert len(c.calls)==4

def test_validated_exact_dictionary_skips_model(tmp_path):
    c=Client();p=Pipeline({'fingerprint':'test','titles':{'謎のフィギュア':{'ko':'피규어','context':{'manufacturer':'TAITO','franchise':None,'product_line':None}}}},c,tmp_path)
    assert p.translate(source())['method']=='validated_dictionary'
    assert c.calls==[]

def test_same_title_in_another_context_does_not_reuse_dictionary(tmp_path):
    c=Client();p=Pipeline({'fingerprint':'test','titles':{'謎のフィギュア':{'ko':'피규어','context':{'manufacturer':'Other','franchise':'Other work','product_line':None}}}},c,tmp_path)
    assert p.translate(source())['method']=='translation_model'
    assert len(c.calls)==1

def test_classification_dictionary_skips_model_and_has_evidence(tmp_path,monkeypatch):
    import app.services.split_semantics as service
    entity={'original':'フェルン','ko':'페른','evidence_field':'name_original','evidence':'フェルン','confidence':1}
    work={**entity,'original':'葬送のフリーレン','ko':'장송의 프리렌','evidence':'葬送のフリーレン'}
    form={'code':'scale_figure','evidence_field':'scale','evidence':'1/7','confidence':1}
    monkeypatch.setattr(service,'candidates',lambda s,groups=None:{'franchise':work,'characters':[entity],'figure_form':form})
    monkeypatch.setattr(service,'title_hints',lambda s,g,groups=None:[])
    c=Client();p=pipeline(tmp_path,c)
    assert p.classify(source(),{'name_ko':'페른 피규어'})['method']=='dictionary'
    assert c.calls==[]

def test_changed_source_invalidates_translation_stage(tmp_path):
    c=Client();p=pipeline(tmp_path,c);p.translate(source());p.translate({**source(),'scale':'1/7'})
    assert len(c.calls)==2

def test_evidence_windows_are_literal_not_translated():
    s={**source(),'document_0':'x'*40000+'作品名: 原作 A キャラクター: 名前 B'+'y'*40000}
    out=classification_input(s)
    assert len(out['document_0'])<1000
    assert all(piece in s['document_0'] for piece in out['document_0'].split('\n'))

def test_explicit_document_relationship_supplies_work_and_scoped_character():
    from app.services.split_semantics import grounded_dictionary
    from app.services.semantic_rules import validate_result
    s={**source(),'name_original':'ねんどろいど ナヒーダ',
       'document_0':'『原神』より、スメールの草神「ナヒーダ」がねんどろいどになって登場'}
    d={'domain_groups':[{'work':'원신','aliases':['原神'],'characters':[['ナヒーダ','나히다']]}]}
    g=grounded_dictionary(s,d)
    assert g['franchise']['ko']=='원신' and g['characters'][0]['ko']=='나히다'
    fields,issues=validate_result(s,{'name_ko':'넨도로이드 나히다',**g})
    assert fields['classification_status']=='ready' and not issues
    other={**s,'document_0':None,'name_original':'ねんどろいど ナヒーダ'}
    assert not grounded_dictionary(other,d)['franchise']

def test_korean_action_figure_has_same_validation_as_japanese():
    from app.services.local_semantic_grounding import explicit_form
    from app.services.semantic_rules import validate_result
    s={**source(),'name_original':'테스트 액션 피규어'}
    f,issues=validate_result(s,{'name_ko':s['name_original'],'franchise':None,'characters':[],'figure_form':explicit_form(s)})
    assert f['figure_form']=='action_figure' and 'FORM_KEYWORD_NOT_SUPPORTED' not in issues

def test_conflicting_work_aliases_remain_unresolved():
    from app.services.split_semantics import grounded_dictionary
    s={**source(),'name_original':'ねんどろいど 名前','document_0':'『未確認作品』より、「名前」が登場'}
    d={'domain_groups':[{'work':'작품 하나','aliases':['未確認作品'],'characters':[]},
                        {'work':'작품 둘','aliases':['未確認作品'],'characters':[]}]}
    assert grounded_dictionary(s,d)['franchise'] is None

def test_normalized_work_title_and_scoped_character_compose_without_translation_model(tmp_path):
    c=Client();p=pipeline(tmp_path,c)
    s={**source(),'name_original':'無職転生III ~異世界行ったら本気だす~ Desktop Cute フィギュア エリス・グレイラット~チャイナドレスver.~'}
    translated=p.translate(s)
    assert translated['method']=='dictionary_composition' and c.calls==[]
    assert translated['name_ko'].count('이세계')==1
    assert '데스크톱 큐트' in translated['name_ko'] and '차이나 드레스 버전' in translated['name_ko']
    class Duplicate(Client):
        def infer(self,*args):
            return {'franchise':None,'figure_form':None,'characters':[{'original':'エリス','ko':'エリス','evidence_field':'name_original','evidence':'エリス','confidence':1}]},{'seconds':0}
    p=pipeline(tmp_path/'duplicate',Duplicate())
    classified=p.classify(s,translated)
    assert all(c['ko']!='エリス' for c in classified['result']['characters'])

@pytest.mark.parametrize('failed_stage',['translation','classification'])
def test_worker_continues_after_one_item_failure(tmp_path,monkeypatch,failed_stage):
    from types import SimpleNamespace
    import scripts.split_semantics_worker as worker
    class DB:
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def get(self,model,fid):return SimpleNamespace(id=fid)
    class FakePipeline:
        def __init__(self,*args):
            self.translation_model='translate';self.classification_model='classify';self.digests={'translate':'a','classify':'b'}
        def translate(self,source):
            if failed_stage=='translation' and source['name_original']=='1':raise ValueError('item failure')
            return {'name_ko':'번역'}
        def classify(self,source,translation):
            if failed_stage=='classification' and source['name_original']=='1':raise ValueError('item failure')
            return {'result':{'franchise':None,'characters':[],'figure_form':None}}
    path=tmp_path/'reference/semantic_dictionary';path.mkdir(parents=True)
    (path/'catalog.json').write_text(json.dumps({'fingerprint':'test'}))
    monkeypatch.setattr(worker,'get_settings',lambda:SimpleNamespace(data_dir=tmp_path))
    monkeypatch.setattr(worker,'SessionLocal',DB)
    monkeypatch.setattr(worker,'Pipeline',FakePipeline)
    monkeypatch.setattr(worker,'source_of',lambda f:{'name_original':str(f.id)})
    monkeypatch.setattr(worker,'source_hash',lambda s:s['name_original'])
    monkeypatch.setattr(worker,'validate_result',lambda *args:({},[]))
    monkeypatch.setattr(worker,'save_record',lambda *args:'partial')
    result=worker.consume(2,tmp_path/'reports',ids=[1,2],client=object())
    assert result['failed']==1 and result['committed']==1
    assert (tmp_path/'reports/items/1.json').exists()
    assert json.loads((tmp_path/'reports/items/2.json').read_text())['committed']

@pytest.mark.parametrize('explicit',[False,True])
def test_skipped_failures_are_preserved_and_only_explicitly_retried(tmp_path,monkeypatch,explicit):
    from types import SimpleNamespace
    import scripts.split_semantics_worker as worker
    class DB:
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def get(self,model,fid):return SimpleNamespace(id=fid)
    translated=[]
    class FakePipeline:
        def __init__(self,*args):
            self.translation_model='t';self.classification_model='c';self.digests={'t':'a','c':'b'}
        def translate(self,source):
            translated.append(source['name_original'])
            raise ValueError('still invalid')
    path=tmp_path/'reference/semantic_dictionary';path.mkdir(parents=True)
    (path/'catalog.json').write_text(json.dumps({'fingerprint':'new-dictionary'}))
    report_dir=tmp_path/'reports';report_dir.mkdir()
    # An old dictionary/pipeline and expired cooldown must not reactivate a skipped item.
    failures={'1':{'time':0,'error':'TRANSLATION_VALIDATION_FAILED','dictionary':'old','pipeline':'old'}}
    (report_dir/'failures.json').write_text(json.dumps(failures))
    monkeypatch.setattr(worker,'get_settings',lambda:SimpleNamespace(data_dir=tmp_path))
    monkeypatch.setattr(worker,'SessionLocal',DB)
    monkeypatch.setattr(worker,'Pipeline',FakePipeline)
    monkeypatch.setattr(worker,'pending_jobs',lambda *args:[SimpleNamespace(error_summary=json.dumps({'figure_id':1}))])
    monkeypatch.setattr(worker,'source_of',lambda f:{'name_original':str(f.id)})
    monkeypatch.setattr(worker,'source_hash',lambda s:s['name_original'])
    result=worker.consume(20,report_dir,ids=[1] if explicit else None,client=object(),skip_failed=True)
    assert result['committed']==0
    assert result['skipped_failed']==(0 if explicit else 1)
    assert translated==(['1'] if explicit else [])
    assert '1' in json.loads((report_dir/'failures.json').read_text())
    if not explicit:
        assert result['state']=='paused_failed'
        assert json.loads((report_dir/'skipped_failures.json').read_text())['items']==failures
