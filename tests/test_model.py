import math
import unittest

from ctc.diagnostics import upper_barriers
from ctc.model import (
    CapabilityParameters,
    SimulationConfig,
    advance_state,
    capability_derivative,
    integrate_capability_epoch,
    simulate,
)
from ctc.scenarios import base_parameters, base_state


class ModelTests(unittest.TestCase):
    def test_common_epoch_sampling(self):
        params = base_parameters()
        config = SimulationConfig(delta_t=0.5, ode_substeps=8, t0=4.0)
        records = simulate(base_state(), params, epochs=6, config=config)
        self.assertEqual([r.n for r in records], list(range(7)))
        self.assertEqual([r.t for r in records], [4.0 + 0.5 * n for n in range(7)])

    def test_model_clock_rejects_overflowed_epoch(self):
        config = SimulationConfig(delta_t=1e308, ode_substeps=1, t0=1e308)
        with self.assertRaises(ArithmeticError):
            simulate(base_state(), base_parameters(), epochs=1, config=config)

    def test_advance_uses_current_epoch_capability_for_discrete_updates(self):
        params = base_parameters()
        state = base_state()
        config = SimulationConfig()
        first = simulate(state, params, epochs=1, config=config)
        self.assertEqual(first[0].state, state)
        self.assertEqual(first[1].state, advance_state(state, params, config))

    def test_capability_stays_positive_on_reference_fixture(self):
        records = simulate(base_state(), base_parameters(), epochs=80)
        self.assertTrue(all(r.state.A > 0.0 and r.state.H > 0.0 for r in records))

    def test_logistic_term_avoids_capability_ratio_overflow(self):
        params = CapabilityParameters(
            A_0=1.0,
            H_0=1.0,
            K_A=5e-324,
            K_H=1.0,
            alpha_A=5e-324,
            alpha_H=1.0,
            gamma_HA=2.0,
            gamma_AH=0.0,
        )
        dA, dH = capability_derivative(1.0, 1.0, params)
        self.assertEqual(dA, 5e-324)
        self.assertEqual(dH, 0.0)

    def test_rk4_weights_stages_before_accumulation(self):
        params = CapabilityParameters(
            A_0=1.0,
            H_0=1.0,
            K_A=1e308,
            K_H=1e308,
            alpha_A=3e307,
            alpha_H=3e307,
            gamma_HA=0.0,
            gamma_AH=0.0,
        )
        A, H = integrate_capability_epoch(
            1.0,
            1.0,
            params,
            SimulationConfig(delta_t=1e-308, ode_substeps=1),
        )
        self.assertTrue(math.isfinite(A) and math.isfinite(H))
        self.assertGreater(A, 1.3)
        self.assertLess(A, 1.4)
        self.assertEqual(A, H)

    def test_reference_trajectory_respects_theoretical_upper_barriers(self):
        params = base_parameters()
        Abar, Hbar = upper_barriers(K_A=params.capability.K_A, K_H=params.capability.K_H, alpha_A=params.capability.alpha_A, alpha_H=params.capability.alpha_H, gamma_HA=params.capability.gamma_HA, gamma_AH=params.capability.gamma_AH)
        records = simulate(base_state(), params, epochs=80)
        self.assertTrue(all(r.state.A <= Abar + 1e-10 for r in records))
        self.assertTrue(all(r.state.H <= Hbar + 1e-10 for r in records))

    def test_timescales_monotone_and_floor_preserved(self):
        params = base_parameters()
        records = simulate(base_state(), params, epochs=80)
        TA = [r.state.T_A for r in records]
        TH = [r.state.T_H for r in records]
        self.assertTrue(all(a >= b for a, b in zip(TA, TA[1:])))
        self.assertTrue(all(a >= b for a, b in zip(TH, TH[1:])))
        self.assertTrue(all(x >= params.timescale.T_A_min for x in TA))
        self.assertTrue(all(x >= params.timescale.T_H_min for x in TH))

    def test_delta_t_change_does_not_silently_rescale_discrete_coefficients(self):
        params = base_parameters()
        state = base_state()
        a = advance_state(state, params, SimulationConfig(delta_t=1.0, ode_substeps=16))
        b = advance_state(state, params, SimulationConfig(delta_t=0.5, ode_substeps=16))
        self.assertEqual(a.T_A, b.T_A)
        self.assertEqual(a.T_H, b.T_H)
        self.assertEqual(a.B, b.B)
        self.assertNotEqual(a.A, b.A)
        self.assertNotEqual(a.H, b.H)


if __name__ == "__main__":
    unittest.main()
