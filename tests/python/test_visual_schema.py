"""Check the shipped example against the actual published schema."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / 'skills/scientific-visuals/templates'


@unittest.skipUnless(importlib.util.find_spec('jsonschema'), 'jsonschema unavailable')
class VisualSpecificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from jsonschema import Draft202012Validator
        cls.schema = json.loads((TEMPLATES / 'visual-spec.schema.json').read_text(encoding='utf-8'))
        cls.example = json.loads((TEMPLATES / 'visual-spec.example.json').read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def test_example_is_valid_with_unspecified_dimensions(self):
        self.assertEqual(list(self.validator.iter_errors(self.example)), [])

    def test_missing_provenance_invalid_dimensions_and_extra_fields_fail(self):
        for change in ('missing', 'negative', 'extra'):
            specimen = copy.deepcopy(self.example)
            if change == 'missing':
                del specimen['source']
            elif change == 'negative':
                specimen['display']['width_mm'] = -1
            else:
                specimen['invented_field'] = 'unexpected'
            with self.subTest(change=change):
                self.assertTrue(list(self.validator.iter_errors(specimen)))


if __name__ == '__main__':
    unittest.main()
