import unittest

from ctc.saturation import saturation


class SaturationTests(unittest.TestCase):
    def test_positive_and_bounded(self):
        for reference in (0.1, 1.0, 10.0):
            for value in (0.01, 0.5, 2.0, 100.0):
                s = saturation(reference, value)
                self.assertGreater(s, 0.0)
                self.assertLess(s, 1.0)

    def test_strictly_increasing(self):
        reference = 2.5
        xs = [0.1, 0.2, 0.8, 3.0, 50.0]
        values = [saturation(reference, x) for x in xs]
        self.assertTrue(all(a < b for a, b in zip(values, values[1:])))

    def test_rejects_nonpositive_domain(self):
        with self.assertRaises(ValueError):
            saturation(0.0, 1.0)
        with self.assertRaises(ValueError):
            saturation(1.0, 0.0)


if __name__ == "__main__":
    unittest.main()
