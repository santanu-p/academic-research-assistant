import importlib.util
import unittest

from tools import scientific_visuals as sv

PLOTTING = importlib.util.find_spec("numpy") is not None and importlib.util.find_spec("matplotlib") is not None

@unittest.skipUnless(PLOTTING, "NumPy/Matplotlib unavailable")
class ScientificPlotExtensions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global np, plt
        import numpy as np
        import matplotlib.pyplot as plt

    def tearDown(self):
        plt.close('all')

    def test_pairs_keep_subject_alignment_and_missing_observations(self):
        fig, ax = sv.paired_plot([[1, 3], [2, np.nan], [np.nan, 4]],
                                 ['Before', 'After'], subject_labels=['a', 'b', 'c'])
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], ['Before', 'After'])
        self.assertEqual(len(ax.lines), 3)
        np.testing.assert_allclose(ax.lines[0].get_ydata(), [1, 3])
        self.assertTrue(np.isnan(ax.lines[1].get_ydata()[1]))
        self.assertTrue(np.isnan(ax.lines[2].get_ydata()[0]))
        self.assertEqual({t.get_text() for t in ax.texts}, {'a', 'b', 'c'})

    def test_pairs_reject_wrong_shape_labels_and_infinity(self):
        for values, labels, subjects in [([[1, 2, 3]], ['a', 'b'], None),
                                          ([[1, 2]], ['a'], None),
                                          ([[1, 2]], ['a', 'b'], ['x', 'y']),
                                          ([[1, np.inf]], ['a', 'b'], None),
                                          ([[np.nan, np.nan]], ['a', 'b'], None)]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                sv.paired_plot(values, labels, subject_labels=subjects)

    def test_heatmap_keeps_grid_order_missing_and_scale(self):
        fig, ax = sv.grid_heatmap([[1, np.nan, 3], [4, 5, 6]],
                                  ['x1', 'x2', 'x3'], ['y1', 'y2'],
                                  value_label='Response (m)', vmin=0, vmax=10)
        image = ax.images[0]
        self.assertEqual(image.origin, 'upper')
        self.assertEqual(image.get_clim(), (0, 10))
        self.assertTrue(np.ma.getmaskarray(image.get_array())[0, 1])
        self.assertEqual(image.get_array()[1, 0], 4)
        self.assertEqual([t.get_text() for t in ax.get_xticklabels()], ['x1', 'x2', 'x3'])
        self.assertEqual([t.get_text() for t in ax.get_yticklabels()], ['y1', 'y2'])
        self.assertEqual(fig.axes[1].get_ylabel(), 'Response (m)')

    def test_heatmap_rejects_explicit_limits_that_hide_extreme_values(self):
        with self.assertRaises(ValueError):
            sv.grid_heatmap([[1, 12]], ['a', 'b'], ['row'], vmin=0, vmax=10)
        with self.assertRaises(ValueError):
            sv.grid_heatmap([[-1, 5]], ['a', 'b'], ['row'], vmin=0, vmax=10)

    def test_heatmap_rejects_misalignment_infinity_and_bad_limits(self):
        for grid, x, y, kwargs in [([[1, 2]], ['a'], ['r'], {}),
                                   ([[1, 2]], ['a', 'b'], ['r', 's'], {}),
                                   ([[1, np.inf]], ['a', 'b'], ['r'], {}),
                                   ([[np.nan]], ['a'], ['r'], {}),
                                   ([[1]], ['a'], ['r'], {'vmin': 2, 'vmax': 1})]:
            with self.subTest(grid=grid, kwargs=kwargs), self.assertRaises(ValueError):
                sv.grid_heatmap(grid, x, y, **kwargs)


if __name__ == '__main__':
    unittest.main()
