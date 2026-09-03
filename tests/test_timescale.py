import unittest

from ctc.saturation import saturation
from ctc.timescale import next_interval, transformed_outcome


class TimescaleTests(unittest.TestCase):
    def test_floor_preserved_and_strict_compression(self):
        floor = 2.0
        value = 12.0
        for _ in range(60):
            nxt = next_interval(current=value, floor=floor, eta=0.05, xi=0.1, exposure=0.6)
            self.assertGreaterEqual(nxt, floor)
            if value > floor:
                self.assertLess(nxt, value)
            value = nxt

    def test_converges_toward_floor(self):
        floor = 3.0
        value = 20.0
        distances = []
        for _ in range(120):
            distances.append(value - floor)
            value = next_interval(current=value, floor=floor, eta=0.08, xi=0.04, exposure=0.5)
        self.assertTrue(all(a >= b for a, b in zip(distances, distances[1:])))
        self.assertLess(value - floor, 0.001)

    def test_tiny_positive_rate_never_rounds_upward(self):
        current = 0.9
        nxt = next_interval(current=current, floor=0.3, eta=1e-20, xi=0.0, exposure=0.0)
        self.assertGreaterEqual(nxt, 0.3)
        self.assertLessEqual(nxt, current)

    def test_cross_exposure_strengthens_compression_above_floor(self):
        low = next_interval(current=10.0, floor=2.0, eta=0.05, xi=0.2, exposure=0.1)
        high = next_interval(current=10.0, floor=2.0, eta=0.05, xi=0.2, exposure=0.9)
        self.assertLess(high, low)

    def test_floor_is_pinned(self):
        self.assertEqual(next_interval(current=2.0, floor=2.0, eta=0.05, xi=0.2, exposure=0.9), 2.0)

    def test_transformed_outcome_matches_eta_plus_xi_s(self):
        current = 11.0
        floor = 2.0
        eta = 0.07
        xi = 0.15
        s = saturation(1.5, 2.0)
        nxt = next_interval(current=current, floor=floor, eta=eta, xi=xi, exposure=s)
        y = transformed_outcome(current=current, nxt=nxt, floor=floor)
        self.assertAlmostEqual(y, eta + xi * s, places=13)

    def test_transformed_outcome_rejects_exact_floor(self):
        with self.assertRaises(ValueError):
            transformed_outcome(current=2.0, nxt=2.0, floor=2.0)


if __name__ == "__main__":
    unittest.main()
