"""Regression checks for the preserved Python MCP implementation."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('python_mcp', ROOT / 'server/assistant_server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class PythonServerTest(unittest.TestCase):
    def call(self, name, arguments):
        reply = server.handle({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                               'params': {'name': name, 'arguments': arguments}})['result']
        self.assertFalse(reply['isError'], reply['content'][0]['text'])
        return json.loads(reply['content'][0]['text'])

    def test_search_current_catalog_and_compatibility_alias(self):
        results = self.call('search_capabilities', {'query': 'scholar-systematic-review'})
        self.assertEqual(results[0]['name'], 'evidence-systematic-review')
        self.assertEqual(results[0]['path'], 'skills/evidence-systematic-review/SKILL.md')

    def test_route_current_rules_and_exact_names(self):
        for task, expected in [
            ('Plan a PRISMA systematic review', 'evidence-systematic-review'),
            ('Humanize this manuscript abstract while preserving equations, citation keys and calibrated uncertainty.', 'academic-humanizer'),
            ('humanizer', 'humanizer'),
            ('scholar-systematic-review', 'evidence-systematic-review'),
        ]:
            with self.subTest(task=task):
                self.assertEqual(self.call('route_task', {'task': task})['skills'][0]['name'], expected)

    def test_current_routing_fixture_primary_selections(self):
        cases = json.loads((ROOT / 'tests/fixtures/routing.json').read_text(encoding='utf-8'))
        for case in cases:
            with self.subTest(task=case['request']):
                result = self.call('route_task', {'task': case['request']})
                self.assertEqual(result['skills'][0]['name'], case['primary'])

    def test_shared_negation_cases(self):
        cases = json.loads((ROOT / 'tests/fixtures/routing-negation-cases.json').read_text(encoding='utf-8'))
        for case in cases:
            with self.subTest(task=case['request']):
                result = self.call('route_task', {'task': case['request']})
                names = [skill['name'] for skill in result['skills']]
                if case['kind'] == 'control':
                    self.assertEqual(names[0], case['expected'])
                else:
                    for name in case['prohibited']:
                        self.assertNotIn(name, names)
                        self.assertNotIn(name, result['alternatives'])
                    if case.get('clarification'):
                        self.assertTrue(result['needs_clarification'])
                    if case.get('preferred') and names[0] != case['preferred']:
                        self.assertEqual(names[0], 'research-assistant')
                        self.assertTrue(result['needs_clarification'])

    def test_editable_powerpoint_poster_and_scientific_table_routing(self):
        for task, expected in [
            ('Design a research poster as an editable PowerPoint slide', 'academic-pptx'),
            ('Create a conference poster in PPTX', 'academic-pptx'),
            ('Make a scientific table of these results', 'visuals-scientific-visual-table-style'),
            ('Build a conference poster using LaTeX', 'latex-academic-poster'),
        ]:
            with self.subTest(task=task):
                self.assertEqual(self.call('route_task', {'task': task})['skills'][0]['name'], expected)
        poster = self.call('route_task', {'task': 'Design a research poster as an editable file'})
        self.assertNotEqual(poster['matched_rule'], 'artifact-artifact-scientific-visuals')

    def test_ambiguous_annotation_request_asks_for_clarification(self):
        result = self.call('route_task', {'task': 'Write annotated bibliography annotations for these papers.'})
        self.assertEqual(result['skills'][0]['name'], 'scholar-literature-review')
        self.assertTrue(result['needs_clarification'])
        self.assertIn('evidence-citations-and-references', result['alternatives'])

    def test_verify_sources_checks_reviewed_mappings(self):
        result = self.call('verify_sources', {})
        self.assertTrue(result['passed'], result)
        self.assertEqual(result['verified'], 600)

    def test_verify_sources_reports_modified_and_missing_files(self):
        with tempfile.TemporaryDirectory(prefix='.test-python-server-', dir=ROOT / 'tests') as tmp:
            root = Path(tmp)
            (root / 'audit/review-118').mkdir(parents=True)
            (root / 'present.txt').write_bytes(b'changed')
            entries = [{'preserved_at': name, 'sha256': hashlib.sha256(b'original').hexdigest()}
                       for name in ('present.txt', 'missing.txt')]
            (root / 'audit/review-118/file-mapping.json').write_text(json.dumps(entries), encoding='utf-8')
            old_root = server.ROOT
            server.ROOT = root
            try:
                result = self.call('verify_sources', {})
            finally:
                server.ROOT = old_root
            self.assertFalse(result['passed'])
            self.assertEqual(result['missing'], ['missing.txt'])
            self.assertEqual(result['mismatched'], ['present.txt'])

    @unittest.skipUnless(sys.platform == 'win32', 'Windows extended-length paths')
    def test_long_windows_path_verification_and_resource_read(self):
        extended_tests = '\\\\?\\' + str(ROOT / 'tests')
        with tempfile.TemporaryDirectory(prefix='.test-long-', dir=extended_tests) as tmp:
            root = Path(tmp[4:])
            relative = 'docs/' + '/'.join(['longcomponent' * 5] * 4) + '/sample.txt'
            extended_file = Path('\\\\?\\' + str(root / relative))
            extended_file.parent.mkdir(parents=True)
            extended_file.write_bytes(b'long path content')
            entries = [{'preserved_at': relative,
                        'sha256': hashlib.sha256(b'long path content').hexdigest()}]
            old_root = server.ROOT
            server.ROOT = root
            try:
                report = server.verify_entries(root, entries)
                self.assertTrue(report['passed'], report)
                self.assertEqual(report['verified'], 1)
                result = server.read_resource(relative)
                self.assertEqual(result['path'], relative)
                self.assertEqual(result['text'], 'long path content')
                for escape in ('../secret', r'C:\secret', r'\\server\share\secret',
                               r'\\?\C:\secret', 'docs/../../secret'):
                    with self.subTest(escape=escape), self.assertRaises(ValueError):
                        server.contained_path(root, escape)
            finally:
                server.ROOT = old_root

    @unittest.skipUnless(sys.platform == 'win32', 'Windows extended-length paths')
    def test_extended_windows_roots_support_drive_unc_and_existing_prefixes(self):
        for root, expected in [
            (r'C:\plugin', r'\\?\C:\plugin'),
            (r'\\server\share\plugin', r'\\?\UNC\server\share\plugin'),
            (r'\\?\C:\plugin', r'\\?\C:\plugin'),
            (r'\\?\UNC\server\share\plugin', r'\\?\UNC\server\share\plugin'),
        ]:
            with self.subTest(root=root):
                self.assertEqual(str(server.filesystem_root(Path(root))), expected)

    def test_resource_reads_reject_non_runtime_and_excluded_paths(self):
        self.assertIn('Academic Research Assistant', self.call('read_resource', {'path': 'README.md'})['text'])
        with tempfile.TemporaryDirectory(prefix='.test-resource-', dir=ROOT / 'tests') as tmp:
            root=Path(tmp)
            names=('tests/fixtures/routing.json', '.private-archive/secret.txt',
                   'docs/.test-secret.txt', 'docs/__pycache__/secret.pyc')
            for name in names:
                target=root/name
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text('private content',encoding='utf-8')
            old_root=server.ROOT
            server.ROOT=root
            try:
                for name in names:
                    with self.subTest(path=name):
                        result = server.handle({'jsonrpc':'2.0','id':1,'method':'tools/call',
                            'params':{'name':'read_resource','arguments':{'path':name}}})['result']
                        self.assertTrue(result['isError'])
            finally:
                server.ROOT=old_root

    def test_resource_reads_reject_symlink_inside_public_directory(self):
        with tempfile.TemporaryDirectory(prefix='.test-resource-', dir=ROOT / 'tests') as tmp:
            root=Path(tmp)
            (root/'docs').mkdir()
            (root/'private.txt').write_text('private', encoding='utf-8')
            try:
                (root/'docs/link.txt').symlink_to(root/'private.txt')
            except OSError as error:
                self.skipTest(f'symbolic links unavailable: {error}')
            old_root=server.ROOT
            server.ROOT=root
            try:
                with self.assertRaises(ValueError):
                    server.read_resource('docs/link.txt')
            finally:
                server.ROOT=old_root

    def test_resource_reads_reject_case_and_windows_path_aliases(self):
        with tempfile.TemporaryDirectory(prefix='.test-alias-', dir=ROOT/'tests') as tmp:
            root=Path(tmp)
            files=('docs/.GIT/secret.txt','docs/.TEST-secret.txt','docs/file.PYC',
                   'resources/upstream/academic-humanizer-main/.gitignore',
                   'skills/academic-humanizer/.gitignore')
            for name in files:
                target=root/name
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text('excluded',encoding='utf-8')
            names=list(files)
            if sys.platform=='win32':
                names.extend(['resources/upstream/academic-humanizer-main/.gitignore.',
                              'skills/academic-humanizer/.GITIGNORE ',
                              'docs/.GIT./secret.txt'])
            old_root=server.ROOT
            server.ROOT=root
            try:
                for name in names:
                    with self.subTest(path=name):
                        with self.assertRaises(ValueError):
                            server.read_resource(name)
            finally:
                server.ROOT=old_root

    def test_bounded_input_discards_oversized_line_and_recovers(self):
        class BoundedInput(io.BytesIO):
            def __iter__(self):
                raise AssertionError('unbounded iteration on stdin')
            def readline(self, size=-1):
                if size < 0 or size > 1024*1024+2:
                    raise AssertionError('unbounded line read')
                return super().readline(size)
        class Stream:
            def __init__(self, buffer):
                self.buffer=buffer
        incoming=BoundedInput(b'x'*(2*1024*1024)+b'\n'+b'{"jsonrpc":"2.0","id":2,"method":"ping"}\n')
        outgoing=io.BytesIO()
        old_stdin,old_stdout=sys.stdin,sys.stdout
        sys.stdin,sys.stdout=Stream(incoming),Stream(outgoing)
        try:
            server.main()
        finally:
            sys.stdin,sys.stdout=old_stdin,old_stdout
        replies=[json.loads(line) for line in outgoing.getvalue().splitlines()]
        self.assertEqual(replies[0]['error']['code'], -32600)
        self.assertEqual(replies[1], {'jsonrpc':'2.0','id':2,'result':{}})

    def test_surrogate_id_does_not_terminate_stdio_server(self):
        incoming=b'{"jsonrpc":"2.0","id":"\\ud800","method":"ping"}\n{"jsonrpc":"2.0","id":2,"method":"ping"}\n'
        result=subprocess.run([sys.executable,'-B',str(ROOT/'server/assistant_server.py')],
                              input=incoming,capture_output=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr.decode('utf-8',errors='replace'))
        replies=[json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(replies[-1],{'jsonrpc':'2.0','id':2,'result':{}})

    def test_deep_json_does_not_terminate_stdio_server(self):
        incoming=b'['*50000+b']'*50000+b'\n{"jsonrpc":"2.0","id":2,"method":"ping"}\n'
        result=subprocess.run([sys.executable,'-B',str(ROOT/'server/assistant_server.py')],
                              input=incoming,capture_output=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr.decode('utf-8',errors='replace'))
        replies=[json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(replies[0]['error']['code'],-32700)
        self.assertEqual(replies[-1],{'jsonrpc':'2.0','id':2,'result':{}})

    def test_initialize_reports_installed_package_version(self):
        result=server.handle({'jsonrpc':'2.0','id':1,'method':'initialize','params':{}})['result']
        version=json.loads((ROOT/'package.json').read_text(encoding='utf-8'))['version']
        self.assertEqual(result['serverInfo']['version'],version)


if __name__ == '__main__':
    unittest.main()
