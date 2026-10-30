"""Check a locally packed draft from its actual archive and offline installation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
NPM = 'npm.cmd' if os.name == 'nt' else 'npm'

class DraftArtifactTest(unittest.TestCase):
    def test_archive_and_installed_cli(self):
        archive = Path(os.environ['ARA_DRAFT_TARBALL']).resolve(strict=True)
        with tarfile.open(archive, 'r:gz') as packed:
            inventory = json.load(packed.extractfile('package/catalog/files.json'))
            expected = {'package/' + item['path'] for item in inventory} | {'package/catalog/files.json'}
            actual = {member.name for member in packed if member.isfile()}
            self.assertEqual(actual, expected, 'Archive contains missing or unindexed files')
            entries = json.load(packed.extractfile('package/catalog/skills.json'))
            self.assertEqual(len(entries), 90)
            self.assertNotIn('latex-document-workflow', {entry['name'] for entry in entries})
            self.assertFalse(any(name.startswith('package/skills/latex-document-workflow/') for name in packed.getnames()))
            for entry in entries:
                source = (ROOT / entry['path']).read_bytes()
                actual = packed.extractfile('package/' + entry['path']).read()
                self.assertEqual(hashlib.sha256(actual).digest(), hashlib.sha256(source).digest(), entry['path'])
            for rel in ('tools/scientific_visuals.py', 'tools/presentation_builder.py', 'tools/text_revision_report.py',
                        'tools/pipeline_checkpoint.py', 'tools/check_external_skills.mjs', 'tools/external_handoff.mjs',
                        'examples/presentation.json',
                        'skills/systematic-review/templates/screening-flow.md',
                        'skills/scientific-visuals/templates/visual-spec.schema.json',
                        'skills/scientific-visuals/templates/visual-spec.example.json',
                        'skills/scientific-visuals/templates/research-table.tex',
                        'skills/scientific-visuals/templates/research-table.html'):
                self.assertEqual(packed.extractfile('package/' + rel).read(), (ROOT / rel).read_bytes(), rel)
            mapping = json.load(packed.extractfile('package/docs/humanizer-source-map.json'))
            self.assertEqual(len(mapping), 24)
            for item in mapping:
                actual = packed.extractfile('package/' + item['destination']).read()
                self.assertEqual(hashlib.sha256(actual).hexdigest(), item['sha256'], item['destination'])
        with tempfile.TemporaryDirectory(prefix='.test-draft-artifact-', dir=ROOT.parent) as temporary:
            project = Path(temporary) / 'consumer'
            project.mkdir()
            (project / 'package.json').write_text('{"private":true}\n', encoding='utf-8')
            cache = Path(temporary) / 'npm-cache'
            install = subprocess.run([NPM, 'install', '--offline', '--ignore-scripts', '--no-audit',
                                      '--no-fund', '--cache', str(cache), str(archive)], cwd=project,
                                     capture_output=True, text=True, encoding='utf-8', timeout=120)
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
            installed = project / 'node_modules/academic-research-assistant'
            for item in mapping:
                actual = (installed / item['destination']).read_bytes()
                self.assertEqual(hashlib.sha256(actual).hexdigest(), item['sha256'], item['destination'])
            binary = installed / 'cli/ara.mjs'
            def run(*args):
                result = subprocess.run(['node', str(binary), *args], cwd=project,
                                        capture_output=True, text=True, encoding='utf-8', timeout=60)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return json.loads(result.stdout)
            self.assertTrue(run('verify')['passed'])
            self.assertEqual(run('route', 'systematic-review-protocol')['skills'][0]['name'],
                             'systematic-review-protocol')
            self.assertEqual(run('route', 'Humanize my manuscript abstract while preserving citations')['skills'][0]['name'],
                             'academic-humanizer')
            self.assertEqual(run('route', 'Humanize my email to a colleague')['skills'][0]['name'], 'humanizer')
            self.assertEqual(run('route', 'Explain a confidence interval and odds ratio')['skills'][0]['name'],
                             'statistical-analysis')
            self.assertIn('document-conversion',
                          [skill['name'] for skill in run('route', 'Convert this CSV to a LaTeX table')['skills'][:3]])
            excluded = run('route', 'Do not humanize my manuscript; check citations')
            self.assertTrue(excluded['skills'])
            self.assertFalse({'humanizer', 'academic-humanizer'} & {skill['name'] for skill in excluded['skills']})
            self.assertTrue(any('citation' in skill['name'] or 'bibliograph' in skill['name']
                                for skill in excluded['skills']))
            resource = run('read', 'skills/latex-beamer-presentations/SKILL.md')
            self.assertIn('Beamer', resource['text'])
            worksheet = run('read', 'skills/systematic-review/templates/screening-flow.md')
            self.assertIn('Retrieval pending', worksheet['text'])
            contrast = subprocess.run([sys.executable, '-S', '-B', '-c',
                'from tools.scientific_visuals import contrast_ratio; print(contrast_ratio("#000", "#fff"))'],
                cwd=installed, capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(contrast.returncode, 0, contrast.stdout + contrast.stderr)
            self.assertEqual(float(contrast.stdout.strip()), 21.0)
            presentation_help = subprocess.run([sys.executable, '-B', str(installed / 'tools/presentation_builder.py'), '--help'],
                                               capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(presentation_help.returncode, 0, presentation_help.stderr)
            self.assertIn('output', presentation_help.stdout)
            old_text, new_text = project / 'before.txt', project / 'after.txt'
            report_path = project / 'comparison.html'
            old_text.write_text('The effect was large.\n', encoding='utf-8')
            new_text.write_text('The effect was uncertain.\n', encoding='utf-8')
            comparison = subprocess.run([sys.executable, '-B', str(installed / 'tools/text_revision_report.py'),
                                         str(old_text), str(new_text), str(report_path)],
                                        capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(comparison.returncode, 0, comparison.stdout + comparison.stderr)
            self.assertIn('<del title="Deleted">large.</del>', report_path.read_text(encoding='utf-8'))
            self.assertIn('<ins title="Added">uncertain.</ins>', report_path.read_text(encoding='utf-8'))
            checkpoint = project / 'checkpoint.json'
            checkpoint.write_text(json.dumps({'phases': [{'id': 'next', 'state': 'pending', 'depends_on': []}]}), encoding='utf-8')
            checked = subprocess.run([sys.executable, '-B', str(installed / 'tools/pipeline_checkpoint.py'), str(checkpoint)],
                                     capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertEqual(json.loads(checked.stdout)['phases'][0]['effective_state'], 'pending')
            external = project / 'external-skills.json'
            external.write_text(json.dumps({'version': 1, 'skills': [{'name': 'sample',
                                'path': str(installed / 'skills/latex-beamer-presentations')}]}), encoding='utf-8')
            preflight = subprocess.run(['node', str(installed / 'tools/check_external_skills.mjs'), str(external)],
                                       capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(preflight.returncode, 0, preflight.stderr)
            self.assertEqual(json.loads(preflight.stdout)['results'][0]['status'], 'readable')
            handoff = project / 'handoff.json'
            handoff.write_text(json.dumps({'version': 1, 'capabilities': [],
                                'steps': [{'id': 'prepare', 'action': 'Prepare draft', 'status': 'pending',
                                           'dependsOn': [], 'requires': []}]}), encoding='utf-8')
            handoff_check = subprocess.run(['node', str(installed / 'tools/external_handoff.mjs'), str(handoff)],
                                           capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(handoff_check.returncode, 0, handoff_check.stderr)
            self.assertEqual(json.loads(handoff_check.stdout)['results'][0]['assessment'], 'ready-for-host')
            for host in ('codex', 'claude', 'antigravity'):
                exported = run('export', '--host', host, '--target', str(Path(temporary) / (host + ' export')))
                bundle = Path(exported['bundle'])
                catalog = json.loads((bundle / 'catalog/skills.json').read_text(encoding='utf-8'))
                self.assertEqual(len(catalog), 90, host)
                self.assertNotIn('latex-document-workflow', {entry['name'] for entry in catalog}, host)
                self.assertFalse((bundle / 'skills/latex-document-workflow').exists(), host)
                self.assertTrue(all((bundle / entry['path']).is_file() for entry in catalog), host)
                verify = subprocess.run(['node', str(bundle / 'cli/ara.mjs'), 'verify'],
                                        capture_output=True, text=True, encoding='utf-8', timeout=60)
                self.assertEqual(verify.returncode, 0, verify.stderr)
                self.assertTrue(json.loads(verify.stdout)['passed'], host)
            result = subprocess.run([NPM, 'exec', '--offline', '--cache', str(cache), '--',
                                     'academic-research-assistant', 'verify'], cwd=project,
                                    capture_output=True, text=True, encoding='utf-8', timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)['passed'])

if __name__ == '__main__':
    unittest.main()
