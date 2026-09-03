import math
import unittest

from ctc.diagnostics import Equilibrium, JacobianTerms, find_interior_equilibrium, jacobian_terms, phi, psi, upper_barriers


class DiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.kw = dict(A_0=1.4, H_0=1.8, K_A=8.0, K_H=7.0, alpha_A=0.22, alpha_H=0.16, gamma_HA=0.12, gamma_AH=0.10)

    def test_equilibrium_witness_satisfies_nullclines_and_bounds(self):
        eq = find_interior_equilibrium(**self.kw)
        Abar, Hbar = upper_barriers(K_A=self.kw["K_A"], K_H=self.kw["K_H"], alpha_A=self.kw["alpha_A"], alpha_H=self.kw["alpha_H"], gamma_HA=self.kw["gamma_HA"], gamma_AH=self.kw["gamma_AH"])
        A_rhs = phi(H=eq.H, K_A=self.kw["K_A"], alpha_A=self.kw["alpha_A"], gamma_HA=self.kw["gamma_HA"], H_0=self.kw["H_0"])
        H_rhs = psi(A=eq.A, K_H=self.kw["K_H"], alpha_H=self.kw["alpha_H"], gamma_AH=self.kw["gamma_AH"], A_0=self.kw["A_0"])
        self.assertAlmostEqual(eq.A, A_rhs, places=12)
        self.assertAlmostEqual(eq.H, H_rhs, places=12)
        self.assertGreaterEqual(eq.A, self.kw["K_A"])
        self.assertLessEqual(eq.A, Abar)
        self.assertGreaterEqual(eq.H, self.kw["K_H"])
        self.assertLessEqual(eq.H, Hbar)

    def test_equilibrium_resolves_wide_dynamic_range_bracket(self):
        kw = dict(
            A_0=1.0,
            H_0=1e200,
            K_A=1e-100,
            K_H=1.0,
            alpha_A=1.0,
            alpha_H=1.0,
            gamma_HA=1e100,
            gamma_AH=0.0,
        )
        eq = find_interior_equilibrium(**kw)
        rhs = phi(
            H=eq.H,
            K_A=kw["K_A"],
            alpha_A=kw["alpha_A"],
            gamma_HA=kw["gamma_HA"],
            H_0=kw["H_0"],
        )
        self.assertTrue(math.isclose(eq.A, rhs, rel_tol=1e-15, abs_tol=0.0))
        self.assertLess(eq.A, 1e-90)
        self.assertEqual(eq.H, 1.0)
        with self.assertRaises(RuntimeError):
            find_interior_equilibrium(**kw, iterations=96)

    def test_upper_barrier_and_equilibrium_avoid_ratio_overflow(self):
        kw = dict(
            A_0=1.0,
            H_0=1.0,
            K_A=1e-320,
            K_H=1.0,
            alpha_A=1e-308,
            alpha_H=1.0,
            gamma_HA=1e308,
            gamma_AH=0.0,
        )
        Abar, Hbar = upper_barriers(
            K_A=kw["K_A"], K_H=kw["K_H"],
            alpha_A=kw["alpha_A"], alpha_H=kw["alpha_H"],
            gamma_HA=kw["gamma_HA"], gamma_AH=kw["gamma_AH"],
        )
        self.assertTrue(math.isfinite(Abar))
        self.assertGreater(Abar, 1e295)
        self.assertLess(Abar, 2e296)
        self.assertEqual(Hbar, 1.0)

        eq = find_interior_equilibrium(**kw)
        self.assertTrue(math.isfinite(eq.A))
        self.assertGreaterEqual(eq.A, kw["K_A"])
        self.assertLessEqual(eq.A, Abar)
        self.assertEqual(eq.H, 1.0)

    def test_jacobian_formulas_and_real_eigenvalues(self):
        eq = find_interior_equilibrium(**self.kw)
        jt = jacobian_terms(equilibrium=eq, **self.kw)
        self.assertAlmostEqual(jt.trace, -(jt.p + jt.q))
        self.assertAlmostEqual(jt.determinant, jt.p * jt.q - jt.b * jt.c)
        self.assertAlmostEqual(jt.discriminant, (jt.p - jt.q) ** 2 + 4 * jt.b * jt.c)
        self.assertGreaterEqual(jt.discriminant, 0.0)
        a, b = jt.eigenvalues
        self.assertIsInstance(a, float)
        self.assertIsInstance(b, float)

    def test_jacobian_coupling_denominator_is_scaled(self):
        jt = jacobian_terms(
            equilibrium=Equilibrium(A=1.5, H=1e200),
            A_0=1.0,
            H_0=1e200,
            K_A=1.0,
            K_H=1e200,
            alpha_A=1.0,
            alpha_H=1.0,
            gamma_HA=1.0,
            gamma_AH=0.0,
        )
        self.assertTrue(math.isclose(jt.b, 3.75e-201, rel_tol=1e-15))
        self.assertEqual(jt.c, 0.0)

    def test_eigenvalues_avoid_small_root_cancellation(self):
        jt = JacobianTerms(p=1e16, q=1.0, b=0.0, c=0.0)
        near, far = jt.eigenvalues
        self.assertEqual(near, -1.0)
        self.assertEqual(far, -1e16)
        self.assertTrue(jt.stable)

    def test_eigenvalues_scale_before_discriminant_square(self):
        jt = JacobianTerms(p=1e200, q=1.0, b=0.0, c=0.0)
        near, far = jt.eigenvalues
        self.assertEqual(near, -1.0)
        self.assertEqual(far, -1e200)
        self.assertTrue(jt.stable)
        with self.assertRaises(ValueError):
            _ = jt.discriminant

    def test_decoupled_equilibrium(self):
        kw = dict(self.kw)
        kw["gamma_HA"] = 0.0
        eq = find_interior_equilibrium(**kw)
        self.assertEqual(eq.A, kw["K_A"])


if __name__ == "__main__":
    unittest.main()
