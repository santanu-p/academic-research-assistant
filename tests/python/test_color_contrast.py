"""Color-pair contrast is advisory and uses opaque sRGB values only."""
import unittest

from tools.scientific_visuals import contrast_ratio


class ColorContrastTests(unittest.TestCase):
    def test_known_ratios_and_symmetry(self):
        self.assertAlmostEqual(contrast_ratio('#000000', '#ffffff'), 21.0)
        self.assertAlmostEqual(contrast_ratio('#abc', '#abc'), 1.0)
        self.assertAlmostEqual(contrast_ratio('#777777', '#ffffff'), 4.478089453577214)
        self.assertEqual(contrast_ratio('#ffffff', '#777777'), contrast_ratio('#777777', '#ffffff'))

    def test_rejects_unsupported_or_invalid_colors(self):
        for color in ('white', '#1234', '#12345678', '#GGGGGG', '123456', None):
            with self.subTest(color=color), self.assertRaises(ValueError):
                contrast_ratio(color, '#ffffff')


if __name__ == '__main__':
    unittest.main()
