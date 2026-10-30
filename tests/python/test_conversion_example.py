"""Run the documented CSV-to-TeX example on synthetic values."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ConversionExampleTests(unittest.TestCase):
    def test_values_escaping_and_no_overwrite(self):
        doc = (ROOT / 'skills/document-conversion/SKILL.md').read_text(encoding='utf-8')
        source = doc.split('~~~python\n', 1)[1].split('\n~~~', 1)[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script, data, output = root / 'convert.py', root / 'data.csv', root / 'table.tex'
            script.write_text(source, encoding='utf-8')
            data.write_text('Name,Value (s)\na_b,1.20\nx%y,\n', encoding='utf-8')
            run = lambda: subprocess.run([sys.executable, '-B', str(script), str(data), str(output)],
                                         capture_output=True, text=True, encoding='utf-8')
            result = run()
            self.assertEqual(result.returncode, 0, result.stderr)
            converted = output.read_text(encoding='utf-8')
            self.assertIn(r'a\_b & 1.20', converted)
            self.assertIn(r'x\%y & ', converted)
            self.assertNotEqual(run().returncode, 0)
            self.assertEqual(output.read_text(encoding='utf-8'), converted)


if __name__ == '__main__':
    unittest.main()
