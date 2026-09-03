import unittest

from ctc.verification import backlog_next, load_ratio


class VerificationTests(unittest.TestCase):
    def test_load_equivalence(self):
        cases = [(0.2, 0.4, 1.0, 2.0), (0.5, 0.5, 2.0, 2.0), (0.8, 0.2, 3.0, 1.0)]
        for lam, mu, A, H in cases:
            direct = lam * A <= mu * H
            ratio = load_ratio(lambda_a=lam, mu_h=mu, A=A, H=H) <= 1.0
            self.assertEqual(direct, ratio)

    def test_large_balanced_products_remain_critical(self):
        self.assertEqual(load_ratio(lambda_a=1e308, mu_h=1e308, A=2.0, H=2.0), 1.0)

    def test_large_cancelling_backlog_terms_do_not_form_nan(self):
        self.assertEqual(
            backlog_next(B=4.0, lambda_a=1e308, mu_h=1e308, A=2.0, H=2.0),
            4.0,
        )

    def test_backlog_nonincrease_below_critical_load(self):
        B = 4.0
        nxt = backlog_next(B=B, lambda_a=0.2, mu_h=0.5, A=1.0, H=2.0)
        self.assertLessEqual(nxt, B)

    def test_backlog_increases_above_critical_load(self):
        B = 4.0
        nxt = backlog_next(B=B, lambda_a=0.8, mu_h=0.1, A=3.0, H=1.0)
        self.assertGreater(nxt, B)


if __name__ == "__main__":
    unittest.main()
