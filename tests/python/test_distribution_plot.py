import unittest

from tools import scientific_visuals as sv


class DistributionPlotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.np, cls.plt = sv._dependencies()
        except RuntimeError as exc:
            raise unittest.SkipTest(str(exc))

    def test_every_observation_including_duplicates_is_retained(self):
        fig, ax = sv.distribution_plot([[2, 2, 5], [7]], ['A', 'B'])
        try:
            self.assertEqual([list(c.get_offsets()[:, 1]) for c in ax.collections], [[2, 2, 5], [7]])
            self.assertEqual([t.get_text() for t in ax.get_xticklabels()], ['A', 'B'])
            self.assertNotEqual(ax.collections[0].get_offsets()[0, 0], ax.collections[0].get_offsets()[1, 0])
        finally:
            self.plt.close(fig)

    def test_invalid_groups_are_rejected(self):
        for groups, labels in [([], []), ([[1], []], ['A', 'B']), ([[1, float('nan')]], ['A']),
                               ([[float('inf')]], ['A']), ([[1]], []), ([[1]], [1])]:
            with self.subTest(groups=groups, labels=labels), self.assertRaises(ValueError):
                sv.distribution_plot(groups, labels)

    def test_placement_is_repeatable(self):
        fig1, ax1 = sv.distribution_plot([[3, 4, 5]], ['A'])
        fig2, ax2 = sv.distribution_plot([[3, 4, 5]], ['A'])
        try:
            self.np.testing.assert_array_equal(ax1.collections[0].get_offsets(), ax2.collections[0].get_offsets())
        finally:
            self.plt.close(fig1)
            self.plt.close(fig2)


if __name__ == '__main__':
    unittest.main()
