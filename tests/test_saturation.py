import math
import unittest

from ctc.saturation import saturation, saturation_approx


class SaturationTests(unittest.TestCase):
    def test_positive_and_bounded_on_resolved_inputs(self):
        cases = (
            (0.1, 0.01),
            (0.1, 0.2),
            (1.0, 0.5),
            (1.0, 2.0),
            (10.0, 0.5),
            (10.0, 5.0),
        )
        for reference, value in cases:
            s = saturation(reference, value)
            self.assertGreater(s, 0.0)
            self.assertLess(s, 1.0)

    def test_strictly_increasing_on_accepted_domain(self):
        reference = 2.5
        xs = [0.1, 0.8, 3.0, 50.0]
        values = [saturation(reference, x) for x in xs]
        self.assertTrue(all(a < b for a, b in zip(values, values[1:])))

    def test_adjacent_collision_away_from_symmetry_is_rejected(self):
        value = 10.0
        successor = math.nextafter(value, math.inf)
        self.assertEqual(saturation_approx(1.0, value), saturation_approx(1.0, successor))
        with self.assertRaises(ValueError):
            saturation(1.0, value)

    def test_adjacent_collision_at_symmetry_is_rejected(self):
        reference = 1e-100
        successor = math.nextafter(reference, math.inf)
        self.assertEqual(saturation_approx(reference, reference), 0.5)
        self.assertEqual(saturation_approx(reference, successor), 0.5)
        with self.assertRaises(ValueError):
            saturation(reference, reference)

    def test_large_equal_inputs_do_not_overflow_approximation(self):
        self.assertEqual(saturation_approx(1e308, 1e308), 0.5)

    def test_unrepresentable_open_boundary_is_rejected(self):
        with self.assertRaises(ValueError):
            saturation(1e308, 5e-324)
        with self.assertRaises(ValueError):
            saturation_approx(1e308, 5e-324)

    def test_rejects_nonpositive_domain(self):
        with self.assertRaises(ValueError):
            saturation(0.0, 1.0)
        with self.assertRaises(ValueError):
            saturation(1.0, 0.0)


if __name__ == "__main__":
    unittest.main()
