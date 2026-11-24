import copy
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.entities import Base,Manufacturer,Figure
from app.models.semantics import ProductSemantics
from app.services.product_semantics import source_of,source_hash,validate_result
from app.services.local_title_translation import assemble,title_issues,apply_title,apply_classification,apply_term_hints
from app.services.semantic_errors import SemanticError

def test_parts_cover_all_source_and_preserve_codes():
    original="RUBIK&#039;S ID \u305f\u307e\u3054\u3063\u3061"
    parts=[{'source':"RUBIK'S ID",'ko':"RUBIK'S ID"},{'source':'\u305f\u307e\u3054\u3063\u3061','ko':'\ub2e4\ub9c8\uace0\uce58'}]
    assert assemble(original,parts)=="RUBIK'S ID \ub2e4\ub9c8\uace0\uce58"


def test_exact_title_terms_repair_mixed_kana_without_erasing_unknown_words():
    parts = [{'source': 'ニャンとも大きなニャルト！', 'ko': '냐ん토'},
             {'source': '未知の名前', 'ko': '모델 제안'}]
    fixed = apply_term_hints(parts, [])
    assert fixed[0]['ko'] == '아주 커다란 냐루토!'
    assert fixed[1] == parts[1]
    assert parts[0]['ko'] == '냐ん토'

@pytest.mark.parametrize('parts',[
    [{'source':'ABC','ko':'\uc608\uc2dc'}],
    [{'source':'DEF','ko':'\uc608\uc2dc'},{'source':'ABC','ko':'\uc608\uc2dc'}],
    [{'source':'ABC','ko':'\uc608\uc2dc'},{'source':'ABC','ko':'\uc608\uc2dc'}],
])
def test_omitted_reordered_or_duplicated_source_is_rejected(parts):
    with pytest.raises(SemanticError):assemble('ABC DEF',parts)

def test_numbers_and_names_cannot_disappear():
    source={'name_original':'\u30a8\u30de 1/7\u30b9\u30b1\u30fc\u30eb\u30d5\u30a3\u30ae\u30e5\u30a2'}
    assert 'TITLE_NUMERIC_FACT_CHANGED' in title_issues(source,'\uc5e0\ub9c8 \ud53c\uaddc\uc5b4')
    assert any(v.startswith('CANONICAL_NAME_MISSING') for v in title_issues(source,'\uc544\uc2a4\uce74 1/7 \uc2a4\ucf00\uc77c \ud53c\uaddc\uc5b4',[('\u30a8\u30de','\uc5e0\ub9c8')]))

@pytest.fixture
def catalog():
    engine=create_engine('sqlite://')
    Base.metadata.create_all(engine)
    with Session(engine,expire_on_commit=False) as db:
        maker=Manufacturer(name='Example',name_ko='\uc608\uc2dc',official_url='https://example.com')
        db.add(maker);db.flush()
        f=Figure(manufacturer_id=maker.id,name_original='\u30a8\u30de 1/7\u30b9\u30b1\u30fc\u30eb\u30d5\u30a3\u30ae\u30e5\u30a2',franchise='\u52dd\u5229\u306e\u5973\u795e:NIKKE',official_url='https://example.com/emma',type='figure')
        db.add(f);db.commit()
        source=source_of(f);digest=source_hash(source)
        fields,_=validate_result(source,{'name_ko':None,'franchise':None,'characters':[],'figure_form':None})
        fields['franchise_ko']='\uc2b9\ub9ac\uc758 \uc5ec\uc2e0: \ub2c8\ucf00'
        fields['field_status']['franchise_ko']='ready';fields['field_issues']['franchise_ko']=[]
        fields['character_ko']=None;fields['characters']=[];fields['field_status']['character_ko']='missing'
        db.add(ProductSemantics(figure_id=f.id,source=source,source_hash=digest,fields=fields,status='partial',model='existing',issues=[]));db.commit()
        yield db,f,source,digest
    engine.dispose()

def reviewed():
    return {'name_ko':'\uc5e0\ub9c8 1/7 \uc2a4\ucf00\uc77c \ud53c\uaddc\uc5b4','model':'ollama:test','processing_fingerprint':'test',
      'attempts':[{'draft':{'parts':[{'source':'\u30a8\u30de','ko':'\uc5e0\ub9c8'},{'source':'1/7','ko':'1/7'},{'source':'\u30b9\u30b1\u30fc\u30eb\u30d5\u30a3\u30ae\u30e5\u30a2','ko':'\uc2a4\ucf00\uc77c \ud53c\uaddc\uc5b4'}]},
                  'review':{'approved':True,'issues':[]}}]}

def test_title_fill_preserves_existing_classifications(catalog):
    db,f,source,digest=catalog
    prior=copy.deepcopy(db.get(ProductSemantics,f.id).fields)
    assert apply_title(db,f.id,source,digest,reviewed())=='translated'
    saved=db.get(ProductSemantics,f.id).fields
    assert f.name_ko==reviewed()['name_ko']
    for key in ('franchise_ko','characters','figure_form','classification_overrides'):
        assert saved.get(key)==prior.get(key)
    assert apply_title(db,f.id,source,digest,reviewed())=='already_translated'

def test_unapproved_or_stale_title_cannot_be_published(catalog):
    db,f,source,digest=catalog
    bad=reviewed();bad['attempts'][0]['review']['approved']=False
    with pytest.raises(SemanticError):apply_title(db,f.id,source,digest,bad)
    with pytest.raises(SemanticError):apply_title(db,f.id,source,'stale',reviewed())
    assert f.name_ko is None

def test_classification_refresh_fills_only_empty_fields(catalog):
    db,f,source,digest=catalog
    apply_title(db,f.id,source,digest,reviewed())
    result={'name_ko':None,'franchise':None,'figure_form':None,'characters':[{
        'original':'\u30a8\u30de','ko':'\uc5e0\ub9c8','evidence_field':'name_original','evidence':'\u30a8\u30de','confidence':1}]}
    assert 'character_ko' in apply_classification(db,f.id,source,digest,result,'ollama:test')
    fields=db.get(ProductSemantics,f.id).fields
    assert fields['character_ko']=='\uc5e0\ub9c8'
    assert fields['franchise_ko']=='\uc2b9\ub9ac\uc758 \uc5ec\uc2e0: \ub2c8\ucf00'
    assert fields['name_ko']==reviewed()['name_ko'] and fields['translation_status']=='ready'
