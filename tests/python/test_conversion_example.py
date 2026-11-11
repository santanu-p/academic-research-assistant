"""Run the documented CSV-to-TeX example on synthetic values."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ConversionExampleTests(unittest.TestCase):
    def test_values_escaping_and_no_overwrite(self):
        script = ROOT / 'tools/csv_to_tex.py'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data, output = root / 'data.csv', root / 'table.tex'
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
