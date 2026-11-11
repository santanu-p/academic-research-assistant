"""Behavioral acceptance tests for the real local runtime."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'academic-research-assistant'

def module():
    spec = importlib.util.spec_from_file_location('assistant_server', PACKAGE / 'server/assistant_server.py')
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

class RuntimeTests(unittest.TestCase):
    def test_runtime_is_implemented(self):
        self.assertTrue((PACKAGE / 'server/assistant_server.py').is_file(), 'Local MCP runtime has not been implemented')

    def test_routes_research_lifecycle(self):
        m = module()
        cases = {
            'Plan a PRISMA systematic review': 'evidence-systematic-review',
            'Convert my equations into LaTeX': 'latex-math-equations',
            'Create an academic PowerPoint presentation': 'academic-pptx',
            'Rewrite AI-sounding prose': 'humanizer',
            'Run the full ARMS research pipeline': 'arms-research-pipeline',
            'Plan qualitative interview thematic coding': 'scholar-qualitative-analysis',
            'Write an NIH grant funding proposal': 'scholar-grant-proposal',
            'Format scientific figures and tables': 'visuals-scientific-visual-table-style',
            'Write a point-by-point reviewer response': 'scholar-reviewer-response',
            'Verify my citation references DOI': 'evidence-source-verification',
            'Research ethics informed consent IRB': 'scholar-research-ethics',
            'Conformal prediction mathematical modeling': 'arms-paper-modeler',
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                result = m.route_task(query)
                self.assertIn(expected, [x['name'] for x in result['skills'][:5]])
                self.assertTrue(result['requires_reading_skill'])

    def test_reads_resources_and_rejects_escape(self):
        m = module()
        self.assertIn('Academic', m.read_resource('README.md')['text'])
        for path in ['../goal-objective.md', 'C:/Windows/win.ini', '/etc/passwd', 'resources/../../etc/passwd']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                m.read_resource(path)

    def test_search_returns_overlapping_capabilities(self):
        m = module()
        names = {x['name'] for x in m.search_capabilities('systematic review', limit=30)}
        self.assertIn('evidence-systematic-review', names)
        self.assertIn('scholar-systematic-review', names)

    def test_every_source_skill_is_reachable_by_exact_name(self):
        m=module()
        for skill in m.load_json('catalog/skills.json'):
            with self.subTest(skill=skill['name']):
                self.assertEqual(m.search_capabilities(skill['name'],limit=1)[0]['name'],skill['name'])

    def test_provenance_detects_missing_and_tampered(self):
        m = module()
        temp_root = ROOT / 'work/test-tmp'
        temp_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as tmp:
            base = Path(tmp)
            (base / 'ok').write_bytes(b'hello')
            import hashlib
            entries = [{'destination': 'ok', 'kind': 'file', 'sha256': hashlib.sha256(b'hello').hexdigest()},
                       {'destination': 'missing', 'kind': 'file', 'sha256': '0'*64}]
            report = m.verify_entries(base, entries)
            self.assertEqual(report['verified'], 1)
            self.assertEqual(report['missing'], ['missing'])
            (base / 'ok').write_bytes(b'changed')
            self.assertEqual(m.verify_entries(base, entries)['mismatched'], ['ok'])

    def test_dependency_report_does_not_claim_connections(self):
        m = module()
        result = m.environment_status()
        self.assertEqual(result['external_services'], 'not_configured_by_this_plugin')
        self.assertIn('python', result)

    def test_unknown_tool_and_malformed_call_are_protocol_errors(self):
        m=module()
        for params in [{'name':'absent','arguments':{}}, {'name':[], 'arguments':{}},
                       {'name':'route_task','arguments':[]}, {}]:
            with self.subTest(params=params):
                result=m.handle({'jsonrpc':'2.0','id':10,'method':'tools/call','params':params})
                self.assertIn('error',result)
                self.assertEqual(result['error']['code'],-32602)

    def test_invalid_request_identifiers_do_not_crash_transport(self):
        m=module()
        for rid in [[],{},True,None,1.5,float('nan')]:
            with self.subTest(rid=rid):
                result=m.handle({'jsonrpc':'2.0','id':rid,'method':'ping'})
                self.assertIn('error',result)
                self.assertIsNone(result['id'])

    def test_stdio_discovery_calls_and_errors(self):
        messages = [
            {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'acceptance-test','version':'1'}}},
            {'jsonrpc':'2.0','method':'notifications/initialized'},
            {'jsonrpc':'2.0','id':2,'method':'tools/list'},
            {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'route_task','arguments':{'task':'systematic review PRISMA'}}},
            {'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'read_resource','arguments':{'path':'../escape'}}},
            {'jsonrpc':'2.0','id':5,'method':'unknown'},
            {'jsonrpc':'2.0','id':6,'method':'tools/call','params':{'name':'search_capabilities','arguments':{'query':'review','limit':'bad'}}},
        ]
        p = subprocess.run([sys.executable, str(PACKAGE/'server/assistant_server.py')],
                           input='\n'.join(json.dumps(x) for x in messages)+'\n', capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        rows = [json.loads(x) for x in p.stdout.splitlines()]
        self.assertEqual([x['id'] for x in rows], [1,2,3,4,5,6])
        self.assertEqual(rows[0]['result']['protocolVersion'], '2025-06-18')
        self.assertGreaterEqual(len(rows[1]['result']['tools']), 5)
        self.assertIn('systematic-review', rows[2]['result']['content'][0]['text'])
        self.assertTrue(rows[3]['result']['isError'])
        self.assertEqual(rows[4]['error']['code'], -32601)
        self.assertTrue(rows[5]['result']['isError'])

if __name__ == '__main__':
    unittest.main()
