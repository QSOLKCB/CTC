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


if __name__ == "__main__":
    unittest.main()