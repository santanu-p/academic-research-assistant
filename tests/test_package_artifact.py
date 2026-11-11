"""Verify that an npm package retains every original mapped payload."""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
NPM = 'npm.cmd' if os.name == 'nt' else 'npm'

class PackagePreservationTest(unittest.TestCase):
    def test_npm_pack_includes_all_original_mapped_files(self):
        result = subprocess.run([NPM, 'pack', '--dry-run', '--json', '--ignore-scripts'],
                                cwd=ROOT, text=True, encoding='utf-8', capture_output=True,
                                timeout=120, check=True)
        listing = json.loads(result.stdout)[0]['files']
        included = {item['path'] for item in listing}
        mapping = json.loads((ROOT/'audit/review-118/file-mapping.json').read_text(encoding='utf-8'))
        missing = [row['preserved_at'] for row in mapping if row['preserved_at'] not in included]
        self.assertFalse(missing, 'Original payloads absent from npm artifact: ' + repr(missing))
        self.assertEqual(len(mapping), 600)
        unexpected = [name for name in included if name.startswith('tests/') and
                      not (name.startswith('tests/fixtures/') or
                           name in ('tests/test_package_artifact.py', 'tests/test_python_server.py') or
                           (name.count('/') == 1 and name.endswith('.test.mjs')))]
        self.assertFalse(unexpected, 'Transient test output included in artifact: ' + repr(unexpected))

    def test_actual_tarball_preserves_payload_bytes_and_verifies_after_extraction(self):
        # Keep the destination outside the package so npm cannot pack its own
        # output. No lifecycle hooks or host installation are invoked here.
        with tempfile.TemporaryDirectory(prefix='.test-npm-artifact-', dir=ROOT.parent) as temporary:
            destination = Path(temporary).resolve()
            existing = os.environ.get('ARA_TEST_TARBALL')
            if existing:
                archive = Path(existing).resolve(strict=True)
            else:
                build = subprocess.run(['node', 'dev/build-index.mjs'], cwd=ROOT,
                                       capture_output=True, text=True, timeout=120)
                self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
                result = subprocess.run([NPM, 'pack', '--json', '--ignore-scripts',
                                         '--pack-destination', str(destination)],
                                        cwd=ROOT, text=True, encoding='utf-8', capture_output=True,
                                        timeout=120)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                archive = destination / json.loads(result.stdout)[0]['filename']
            mapping = json.loads((ROOT/'audit/review-118/file-mapping.json').read_text(encoding='utf-8'))
            with tarfile.open(archive, 'r:gz') as packed:
                members = {item.name: item for item in packed.getmembers()}
                for row in mapping:
                    name = 'package/' + row['preserved_at']
                    self.assertIn(name, members, name)
                    payload = packed.extractfile(members[name]).read()
                    self.assertEqual(hashlib.sha256(payload).hexdigest(), row['sha256'], name)
                # Manually extract only regular members under package/. This
                # works on Python 3.10 and rejects traversal and symlinks.
                extracted = destination / 'extracted'
                for member in members.values():
                    self.assertTrue(member.isfile(), member.name)
                    target = extracted.joinpath(*Path(member.name).parts)
                    self.assertTrue(target.resolve().is_relative_to(extracted.resolve()), member.name)
                    self.assertTrue(member.name.startswith('package/'), member.name)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(packed.extractfile(member).read())
            installed = extracted / 'package'
            check = subprocess.run(['node', 'cli/ara.mjs', 'verify'], cwd=installed,
                                   capture_output=True, text=True, encoding='utf-8',
                                   timeout=120)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            self.assertTrue(json.loads(check.stdout)['passed'], check.stdout)

            # Install from the produced tarball without registry access or
            # lifecycle scripts, then exercise the installed npm binary.
            project = destination / 'consumer'
            project.mkdir()
            (project / 'package.json').write_text('{"private":true}\n', encoding='utf-8')
            cache = destination / 'npm-cache'
            install = subprocess.run([NPM, 'install', '--offline', '--ignore-scripts',
                                      '--no-audit', '--no-fund', '--cache', str(cache), str(archive)],
                                     cwd=project, capture_output=True, text=True,
                                     encoding='utf-8', timeout=120)
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
            installed_package = project / 'node_modules' / 'academic-research-assistant-full'
            for row in mapping:
                self.assertEqual(hashlib.sha256((installed_package / row['preserved_at']).read_bytes()).hexdigest(),
                                 row['sha256'], row['preserved_at'])
            python_checks = subprocess.run([sys.executable, '-B', 'tests/test_python_server.py'],
                                           cwd=installed_package, capture_output=True, text=True,
                                           encoding='utf-8', timeout=120)
            self.assertEqual(python_checks.returncode, 0, python_checks.stdout + python_checks.stderr)
            execute = subprocess.run([NPM, 'exec', '--offline', '--cache', str(cache), '--',
                                      'academic-research-assistant-full', 'verify'],
                                     cwd=project, capture_output=True, text=True,
                                     encoding='utf-8', timeout=120)
            self.assertEqual(execute.returncode, 0, execute.stdout + execute.stderr)
            self.assertTrue(json.loads(execute.stdout)['passed'], execute.stdout)
            route = subprocess.run([NPM, 'exec', '--offline', '--cache', str(cache), '--',
                                    'academic-research-assistant-full', 'route',
                                    'Compare these studies and identify evidence gaps'],
                                   cwd=project, capture_output=True, text=True,
                                   encoding='utf-8', timeout=120)
            self.assertEqual(route.returncode, 0, route.stdout + route.stderr)
            self.assertEqual(json.loads(route.stdout)['skills'][0]['name'],
                             'evidence-compare-studies', route.stdout)
            read = subprocess.run([NPM, 'exec', '--offline', '--cache', str(cache), '--',
                                   'academic-research-assistant-full', 'read',
                                   'skills/evidence-compare-studies/SKILL.md'],
                                  cwd=project, capture_output=True, text=True,
                                  encoding='utf-8', timeout=120)
            self.assertEqual(read.returncode, 0, read.stdout + read.stderr)
            self.assertIn('Compare studies in an aligned evidence table', read.stdout)

if __name__ == '__main__':
    unittest.main()
