import copy
import importlib.util
import json
from pathlib import Path
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
import unittest

spec=importlib.util.spec_from_file_location('local',Path(__file__).resolve().parents[1]/'local_semantics.py')
tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)

RESULT={'name_ko':'나루토 이타치 누들 스토퍼','franchise':None,'characters':[],
        'figure_form':{'code':'noodle_stopper','evidence_field':'name_original','evidence':'ぬーどるストッパー','confidence':1}}
SOURCE={'name_original':'NARUTO うちはイタチ ぬーどるストッパー','manufacturer':'FuRyu'}


class Tests(unittest.TestCase):
    def test_shape(self):
        self.assertEqual(tool.validate_shape(RESULT),RESULT)

    def test_missing_keys(self):
        with self.assertRaises(ValueError):tool.validate_shape({'name_ko':'test'})

    def test_boolean_confidence_rejected(self):
        value=copy.deepcopy(RESULT);value['figure_form']['confidence']=True
        with self.assertRaises(ValueError):tool.validate_shape(value)

    def test_evidence(self):
        self.assertEqual(tool.evidence_issues(SOURCE,RESULT),[])
        value=copy.deepcopy(RESULT);value['figure_form']['evidence']='TENITOL'
        self.assertEqual(tool.evidence_issues(SOURCE,value),['figure_form:EVIDENCE_NOT_IN_INPUT'])

    def test_cloud_endpoint_rejected(self):
        with self.assertRaises(ValueError):tool.LocalProvider('https://api.openai.com')
        with self.assertRaises(ValueError):tool.LocalProvider(model='anything:cloud')

    def test_input_bounded_and_secrets_excluded(self):
        value={**SOURCE,'document_0':'あ'*5000,'document_1':'い'*2000,'api_key':'secret'}
        view,truncated=tool.model_input(value)
        self.assertEqual(len(view['document_0']),4000)
        self.assertIsNone(view['document_1'])
        self.assertNotIn('api_key',view)
        self.assertEqual(truncated,['document_0','document_1'])

    def test_report_loader(self):
        self.assertEqual(list(tool.sources_from({'records':[{'figure_id':52,'source':SOURCE}]})),[(52,SOURCE)])

    def test_source_export_loader(self):
        raw={**SOURCE,'id':48,'sources':[{'source_type':'metadata','body':'meta'}, {'source_type':'official_detail','body':'body'}]}
        fid,source=next(tool.sources_from([raw]))
        self.assertEqual(fid,48);self.assertEqual(source['document_0'],'body')

    def test_http_request_and_truncation(self):
        seen=[]
        state={'reason':'stop'}
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                value={'version':'test'} if self.path=='/api/version' else {'models':[{'name':'qwen3:8b','digest':'fixture'}]}
                self.send_response(200);self.end_headers();self.wfile.write(json.dumps(value).encode())
            def do_POST(self):
                seen.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                self.send_response(200);self.end_headers()
                self.wfile.write(json.dumps({'done':True,'done_reason':state['reason'],'message':{'content':json.dumps(RESULT)}}).encode())
            def log_message(self,*a):pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            p=tool.LocalProvider(f'http://127.0.0.1:{server.server_port}')
            self.assertEqual(p.manifest()['digest'],'fixture')
            result,view,meta=p.infer(SOURCE)
            self.assertEqual(result,RESULT)
            self.assertFalse(seen[0]['think']);self.assertFalse(seen[0]['stream'])
            self.assertEqual(seen[0]['format'],tool.schema())
            state['reason']='length'
            with self.assertRaisesRegex(ValueError,'INCOMPLETE'):p.infer(SOURCE)
        finally:server.shutdown();server.server_close();thread.join()


if __name__=='__main__':unittest.main()
