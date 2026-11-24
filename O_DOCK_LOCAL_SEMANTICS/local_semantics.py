"""Bounded local Ollama preview. No application imports, DB writes or paid provider fallback."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
VERSION = 'odock-local-preview-v1'
FORMS = ['noodle_stopper','scale_figure','action_figure','chibi_figure','nendoroid',
         'soft_vinyl','plush','acrylic_stand','mini_figure']
ENTITY_FIELDS = ['name_original','franchise','character','document_0','document_1','document_2']
FORM_FIELDS = ['name_original','product_line','scale','document_0','document_1','document_2']


def schema():
    entity = {'type':'object','additionalProperties':False,'properties':{
        'original':{'type':'string'},'ko':{'type':'string'},
        'evidence_field':{'type':'string','enum':ENTITY_FIELDS},'evidence':{'type':'string'},
        'confidence':{'type':'number','minimum':0,'maximum':1}},
        'required':['original','ko','evidence_field','evidence','confidence']}
    form = {'type':'object','additionalProperties':False,'properties':{
        'code':{'type':'string','enum':FORMS},'evidence_field':{'type':'string','enum':FORM_FIELDS},
        'evidence':{'type':'string'},'confidence':{'type':'number','minimum':0,'maximum':1}},
        'required':['code','evidence_field','evidence','confidence']}
    return {'type':'object','additionalProperties':False,'properties':{
        'name_ko':{'type':'string'},'franchise':{'anyOf':[entity,{'type':'null'}]},
        'characters':{'type':'array','maxItems':20,'items':entity},
        'figure_form':{'anyOf':[form,{'type':'null'}]}},
        'required':['name_ko','franchise','characters','figure_form']}


def validate_shape(result):
    """Transport shape validation only. Existing v4 rules must validate meaning."""
    def keys(value, expected):
        if not isinstance(value,dict) or set(value)!=set(expected): raise ValueError('INVALID_JSON_SHAPE')
    def confidence(value):
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not 0<=value<=1:
            raise ValueError('INVALID_CONFIDENCE')
    def entity(value):
        keys(value,['original','ko','evidence_field','evidence','confidence'])
        if any(not isinstance(value[k],str) or not value[k].strip() for k in ['original','ko','evidence_field','evidence']):
            raise ValueError('EMPTY_ENTITY')
        if value['evidence_field'] not in ENTITY_FIELDS: raise ValueError('INVALID_EVIDENCE_FIELD')
        confidence(value['confidence'])
    keys(result,['name_ko','franchise','characters','figure_form'])
    if not isinstance(result['name_ko'],str) or not result['name_ko'].strip():raise ValueError('EMPTY_NAME')
    if result['franchise'] is not None: entity(result['franchise'])
    if not isinstance(result['characters'],list) or len(result['characters'])>20:raise ValueError('INVALID_CHARACTERS')
    for item in result['characters']: entity(item)
    form=result['figure_form']
    if form is not None:
        keys(form,['code','evidence_field','evidence','confidence'])
        if form['code'] not in FORMS or form['evidence_field'] not in FORM_FIELDS:raise ValueError('INVALID_FORM')
        if not isinstance(form['evidence'],str) or not form['evidence'].strip():raise ValueError('EMPTY_FORM_EVIDENCE')
        confidence(form['confidence'])
    return result


def evidence_issues(source,result):
    issues=[]
    pairs=[('franchise',result['franchise']),('figure_form',result['figure_form'])]
    pairs += [('character',item) for item in result['characters']]
    for field,value in pairs:
        if value is None:continue
        text=source.get(value['evidence_field'])
        if not isinstance(text,str) or value['evidence'] not in text:
            issues.append(field+':EVIDENCE_NOT_IN_INPUT')
        if 'original' in value and value['original'] not in value['evidence']:
            issues.append(field+':ORIGINAL_NOT_IN_EVIDENCE')
    return issues


def model_input(source):
    allowed=['name_original','official_url','manufacturer','manufacturer_ko','product_line',
             'franchise','character','scale','type']
    result={key:source.get(key) for key in allowed}
    if not isinstance(result['name_original'],str) or not result['name_original'].strip():
        raise ValueError('NAME_ORIGINAL_REQUIRED')
    budget=4000
    truncated=[]
    for index in range(3):
        field=f'document_{index}';value=source.get(field)
        if value is not None and not isinstance(value,str):raise ValueError('DOCUMENT_MUST_BE_TEXT')
        text=(value or '')[:budget]
        if len(value or '')>len(text):truncated.append(field)
        result[field]=text or None;budget-=len(text)
    # Do not send secrets/arbitrary DB fields. Oversized titles/metadata are an error.
    if len(json.dumps({k:v for k,v in result.items() if not k.startswith('document_')},ensure_ascii=False))>3000:
        raise ValueError('METADATA_TOO_LARGE')
    return result,truncated


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('REDIRECT_NOT_ALLOWED')


class LocalProvider:
    def __init__(self,base_url='http://127.0.0.1:11434',model='qwen3:8b',timeout=240):
        parsed=urllib.parse.urlsplit(base_url)
        if parsed.scheme!='http' or parsed.hostname not in ('127.0.0.1','localhost','::1','host.docker.internal','ollama'):
            raise ValueError('LOCAL_OLLAMA_ENDPOINT_REQUIRED')
        if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ('','/'):
            raise ValueError('INVALID_LOCAL_ENDPOINT')
        if model.endswith(':cloud') or '-cloud' in model:raise ValueError('CLOUD_MODEL_NOT_ALLOWED')
        self.base_url=base_url.rstrip('/');self.model=model;self.timeout=timeout
        self.opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
        self.instruction=(ROOT/'prompt.txt').read_text(encoding='utf-8')

    def request(self,path,payload=None):
        data=None if payload is None else json.dumps(payload,ensure_ascii=False).encode()
        request=urllib.request.Request(self.base_url+path,data=data,headers={'Content-Type':'application/json'})
        with self.opener.open(request,timeout=self.timeout) as response:
            raw=response.read(2_000_001)
        if len(raw)>2_000_000:raise ValueError('RESPONSE_TOO_LARGE')
        return json.loads(raw)

    def manifest(self):
        tags=self.request('/api/tags')
        found=next((m for m in tags.get('models',[]) if m.get('name')==self.model or m.get('model')==self.model),None)
        if found is None:raise ValueError('LOCAL_MODEL_NOT_INSTALLED')
        version=self.request('/api/version').get('version')
        return dict(ollama_version=version,model=self.model,digest=found.get('digest'),size=found.get('size'),details=found.get('details'))

    def infer(self,source):
        view,truncated=model_input(source)
        payload={'model':self.model,'stream':False,'think':False,'keep_alive':'5m','format':schema(),
                 'options':{'temperature':0,'num_ctx':8192,'num_predict':2048},
                 'messages':[{'role':'system','content':self.instruction},
                             {'role':'user','content':json.dumps({'catalog':view,'output_schema':schema()},ensure_ascii=False)}]}
        started=time.monotonic();raw=self.request('/api/chat',payload)
        if raw.get('done') is not True or raw.get('done_reason')!='stop':raise ValueError('INCOMPLETE_GENERATION')
        if raw.get('error'):raise ValueError('LOCAL_MODEL_ERROR')
        result=validate_shape(json.loads(raw['message']['content']))
        meta={key:raw.get(key) for key in ['prompt_eval_count','eval_count','total_duration','load_duration','done_reason']}
        meta.update(elapsed_seconds=round(time.monotonic()-started,3),truncated_fields=truncated)
        return result,view,meta


def sources_from(data):
    records=data.get('records',[]) if isinstance(data,dict) else data
    if not isinstance(records,list):raise ValueError('INPUT_LIST_REQUIRED')
    for index,item in enumerate(records):
        if not isinstance(item,dict):raise ValueError('RECORD_MUST_BE_OBJECT')
        source=item.get('source',item)
        if not isinstance(source,dict):raise ValueError('SOURCE_MUST_BE_OBJECT')
        # Support the original five-source export and existing semantic report input.
        source=dict(source)
        if 'sources' in source:
            docs=sorted(source['sources'],key=lambda d:d.get('source_type')!='official_detail')[:3]
            for n,doc in enumerate(docs):source[f'document_{n}']=doc.get('body')
            source.pop('sources')
        yield item.get('figure_id',item.get('id',index+1)),source


def atomic(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['health','preview'])
    p.add_argument('--base-url',default='http://127.0.0.1:11434')
    p.add_argument('--model',default='qwen3:8b')
    p.add_argument('--input',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--limit',type=int,default=5)
    args=p.parse_args()
    if not 1<=args.limit<=100:p.error('--limit must be 1..100')
    provider=LocalProvider(args.base_url,args.model)
    manifest=provider.manifest()
    if args.mode=='health':print(json.dumps(manifest,ensure_ascii=False,indent=2));return
    if not args.input or not args.output:p.error('preview requires --input and --output')
    if args.output.exists():p.error('output exists; use a new filename')
    items=list(sources_from(json.loads(args.input.read_text(encoding='utf-8-sig'))))[:args.limit]
    report=dict(mode='LOCAL_PREVIEW_NOT_APPLYABLE',db_committed=False,paid_api_called=False,
                version=VERSION,manifest=manifest,created_at=datetime.now(timezone.utc).isoformat(),
                prompt_sha256=hashlib.sha256(provider.instruction.encode()).hexdigest(),records=[])
    atomic(args.output,report)
    failed=0
    for fid,source in items:
        record=dict(figure_id=fid,source=source,publication_status='not_evaluated')
        try:
            result,view,meta=provider.infer(source)
            record.update(result=result,model_input=view,metrics=meta,transport_status='parsed',
                          evidence_issues=evidence_issues(view,result))
        except Exception as exc:
            record.update(transport_status='failed',error=type(exc).__name__)
            failed+=1
        report['records'].append(record);atomic(args.output,report)
        print(json.dumps({'figure_id':fid,'transport_status':record['transport_status'],
                          'publication_status':'not_evaluated','error':record.get('error')},ensure_ascii=False),flush=True)
        if failed:break  # Avoid repeatedly running a broken server/model configuration.
    report['summary']=dict(Counter(r['transport_status'] for r in report['records']))
    atomic(args.output,report)
    print(json.dumps(dict(mode=report['mode'],summary=report['summary'],output=str(args.output),db_committed=False),ensure_ascii=False))
    if failed:raise SystemExit(1)


if __name__=='__main__':main()
