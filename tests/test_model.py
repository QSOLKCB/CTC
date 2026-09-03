import unittest

from ctc.diagnostics import upper_barriers
from ctc.model import SimulationConfig, advance_state, simulate
from ctc.scenarios import base_parameters, base_state


class ModelTests(unittest.TestCase):
    def test_common_epoch_sampling(self):
        params = base_parameters()
        config = SimulationConfig(delta_t=0.5, ode_substeps=8, t0=4.0)
        records = simulate(base_state(), params, epochs=6, config=config)
        self.assertEqual([r.n for r in records], list(range(7)))
        self.assertEqual([r.t for r in records], [4.0 + 0.5 * n for n in range(7)])

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
