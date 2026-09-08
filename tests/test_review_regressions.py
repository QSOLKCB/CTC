import math
import unittest

from ctc.model import CapabilityParameters, SimulationConfig, integrate_capability_epoch


class ReviewRegressionTests(unittest.TestCase):
    def test_rk4_rejects_reversal_below_K_with_positive_coupling(self):
        params = CapabilityParameters(
            A_0=1.0,
            H_0=1.0,
            K_A=1.0,
            K_H=1.0,
            alpha_A=1.0,
            alpha_H=1.0,
            gamma_HA=1e-20,
            gamma_AH=1e-20,
        )
        with self.assertRaises(ArithmeticError):
            integrate_capability_epoch(
                0.2,
                0.2,
                params,
                SimulationConfig(delta_t=7.7, ode_substeps=1),
            )

    def test_rk4_rejects_reversal_at_K_with_positive_coupling(self):
        params = CapabilityParameters(
            A_0=1.0,
            H_0=1.0,
            K_A=1.0,
            K_H=1.0,
            alpha_A=1.0,
            alpha_H=1.0,
            gamma_HA=0.01,
            gamma_AH=0.01,
        )
        with self.assertRaises(ArithmeticError):
            integrate_capability_epoch(
                1.0,
                1.0,
                params,
                SimulationConfig(delta_t=3.0, ode_substeps=1),
            )

    def test_rk4_rejects_downward_crossing_of_K(self):
        params = CapabilityParameters(
            A_0=1.0,
            H_0=1.0,
            K_A=1.0,
            K_H=1.0,
            alpha_A=1.0,
            alpha_H=1.0,
            gamma_HA=1e-6,
            gamma_AH=1e-6,
        )
        with self.assertRaises(ArithmeticError):
            integrate_capability_epoch(
                1.01,
                1.01,
                params,
                SimulationConfig(delta_t=7.2, ode_substeps=1),
            )

    def test_rk4_rejects_rounded_landing_on_decoupled_K(self):
        params = CapabilityParameters(
            A_0=1.0,
            H_0=1.0,
            K_A=1.0,
            K_H=1.0,
            alpha_A=1.0,
            alpha_H=1.0,
            gamma_HA=0.0,
            gamma_AH=0.0,
        )
        config = SimulationConfig(delta_t=1.0, ode_substeps=1)
        for start in (math.nextafter(1.0, 0.0), math.nextafter(1.0, math.inf)):
            with self.subTest(start=start):
                with self.assertRaises(ArithmeticError):
                    integrate_capability_epoch(start, start, params, config)

    def test_rk4_rejects_coupled_joint_ascent_reversal(self):
        params = CapabilityParameters(
            A_0=1.0,
            H_0=1.0,
            K_A=1.0,
            K_H=1.0,
            alpha_A=1.0,
            alpha_H=1.0,
            gamma_HA=0.01,
            gamma_AH=0.01,
        )
        start = 1.0005012499921877
        with self.assertRaises(ArithmeticError):
            integrate_capability_epoch(
                start,
                start,
                params,
                SimulationConfig(delta_t=2.8, ode_substeps=1),
            )

    def test_rk4_rejects_rounded_landing_on_coupled_upper_barrier(self):
        params = CapabilityParameters(
            A_0=5e-324,
            H_0=5e-324,
            K_A=1.0,
            K_H=1.0,
            alpha_A=1.0,
            alpha_H=1.0,
            gamma_HA=1.0,
            gamma_AH=1.0,
        )
        start = math.nextafter(2.0, 0.0)
        with self.assertRaises(ArithmeticError):
            integrate_capability_epoch(
                start,
                start,
                params,
                SimulationConfig(delta_t=1.0, ode_substeps=1),
            )


if __name__ == "__main__":
    unittest.main()
