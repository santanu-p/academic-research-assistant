"""Exercise packaging with retained source resources and reproducible ZIPs."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import unittest
import zipfile

ROOT = Path(__file__).resolve().parent.parent


class PackageReleaseTest(unittest.TestCase):
    def test_retains_mapped_source_and_builds_reproducible_zip(self):
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as temp:
            base = Path(temp)
            project = base / 'project'
            (project / 'dev').mkdir(parents=True)
            shutil.copyfile(ROOT / 'dev/package-release.py', project / 'dev/package-release.py')
            source = b'MIT source and attribution\n'
            mapping = [{'destination': 'resources/upstream/' + name + '/LICENSE',
                        'sha256': hashlib.sha256(source).hexdigest()}
                       for name in ('humanizer-main', 'academic-humanizer-main')]
            files = {'package.json': b'{"version":"test"}',
                     'resources/upstream/humanizer-main/LICENSE': source,
                     'resources/upstream/academic-humanizer-main/LICENSE': source,
                     'docs/humanizer-source-map.json': json.dumps(mapping).encode()}
            inventory = []
            for name, content in files.items():
                path = project / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                inventory.append({'path': name, 'sha256': hashlib.sha256(content).hexdigest()})
            (project / 'catalog').mkdir()
            (project / 'catalog/files.json').write_text(json.dumps(inventory), encoding='utf-8')
            archive = base / 'draft.tgz'
            with tarfile.open(archive, 'w:gz') as packed:
                for path in project.rglob('*'):
                    if path.is_file() and 'dev' not in path.parts:
                        packed.add(path, arcname='package/' + path.relative_to(project).as_posix())
            results = []
            for attempt in range(2):
                out = base / ('out' + str(attempt))
                result = subprocess.run([sys.executable, str(project / 'dev/package-release.py'),
                                         '--tarball', str(archive), '--out', str(out)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                zipped = out / 'academic-research-assistant-test.zip'
                with zipfile.ZipFile(zipped) as saved:
                    self.assertEqual(saved.read('academic-research-assistant/resources/upstream/humanizer-main/LICENSE'), source)
                results.append(zipped.read_bytes())
                if attempt == 0:
                    time.sleep(2.1)
            self.assertEqual(results[0], results[1])


if __name__ == '__main__':
    unittest.main()
