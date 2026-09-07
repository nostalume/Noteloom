from dataclasses import replace
import unittest

import numpy as np

from fieldcalc.pauli_fierz import PauliFierzRequest, compile_pauli_fierz


class PauliFierzReturnTests(unittest.TestCase):
    def setUp(self):
        self.request = PauliFierzRequest(
            primitive_dimension=28,
            matter_levels=6,
            photon_frequencies=(0.65, 1.10),
            field_coefficients=(0.30, 0.16),
            photon_cutoff=2,
            coupling=0.08,
            resolution=0.20,
            provenance="node 39 frozen Pauli-Fierz bench",
            resource_budget=2_000_000,
        )
        result = compile_pauli_fierz(self.request)
        self.assertTrue(result.accepted, result.refusal)
        self.system = result.system

    def test_one_kinetic_square_generates_linear_and_contact_actions(self):
        receipt = self.system.action_receipt()

        self.assertLess(receipt.expansion_residual, 2e-13)
        self.assertGreater(receipt.linear_norm, 0.0)
        self.assertGreater(receipt.contact_norm, 0.0)

    def test_one_effective_return_matches_the_full_resolvent(self):
        z = self.system.matter_ground_energy + 0.82 + 0.20j
        receipt = self.system.return_receipt(z)

        self.assertLess(receipt.residual, 2e-11)
        self.assertLess(receipt.reduced_operations, receipt.direct_operations)
        self.assertEqual(receipt.reduced_operations, receipt.expert_operations)
        self.assertFalse(receipt.advantage_over_expert)

    def test_contact_and_generated_histories_recover_second_order_return(self):
        z = self.system.matter_ground_energy + 0.82 + 0.20j
        receipt = self.system.second_order_receipt(z)

        self.assertLess(receipt.total_residual, 2e-12)
        self.assertLess(receipt.open_sector_residual, 2e-12)
        self.assertGreater(receipt.contact_norm, 0.0)
        self.assertGreater(receipt.zero_photon_norm, 0.0)
        self.assertGreater(receipt.two_photon_norm, 0.0)

    def test_same_return_generates_bound_pole_and_coherent_open_response(self):
        bound = self.system.bound_receipt()
        incoming = np.array([1.0, 1.0j]) / np.sqrt(2.0)
        outgoing = np.array([1.0, -1.0]) / np.sqrt(2.0)
        opened = self.system.open_receipt(
            self.system.matter_ground_energy + 0.82,
            incoming,
            outgoing,
        )

        self.assertLess(bound.residual, 2e-10)
        self.assertLess(opened.residual, 2e-11)
        self.assertEqual(bound.return_id, opened.return_id)

    def test_matter_and_photon_regulators_do_not_fake_closure(self):
        defects = tuple(
            compile_pauli_fierz(replace(self.request, matter_levels=levels))
            .system.trk_defect
            for levels in (2, 4, 6)
        )
        larger_field = compile_pauli_fierz(replace(
            self.request,
            photon_cutoff=3,
        )).system
        smaller_primitive = compile_pauli_fierz(replace(
            self.request,
            primitive_dimension=20,
        )).system
        base_bound = self.system.bound_receipt().full_energy
        larger_bound = larger_field.bound_receipt().full_energy
        smaller_primitive_bound = smaller_primitive.bound_receipt().full_energy

        self.assertGreater(defects[0], defects[1])
        self.assertGreater(defects[1], defects[2])
        self.assertLess(defects[2], 1e-8)
        self.assertLess(abs(base_bound - larger_bound), 2e-7)
        self.assertLess(abs(base_bound - smaller_primitive_bound), 2e-9)

    def test_invalid_or_underresolved_requests_are_refused(self):
        cases = (
            (replace(self.request, matter_levels=29), "matter level count exceeds primitive basis"),
            (replace(self.request, photon_cutoff=1), "photon cutoff omits order-two sectors"),
            (replace(self.request, field_coefficients=(0.3,)), "field data have different lengths"),
            (replace(self.request, resolution=0.0), "resolution must be positive"),
            (replace(self.request, resource_budget=10), "Pauli-Fierz compilation budget exceeded"),
        )
        for request, reason in cases:
            with self.subTest(reason=reason):
                result = compile_pauli_fierz(request)
                self.assertFalse(result.accepted)
                self.assertEqual(result.refusal.reason, reason)


if __name__ == "__main__":
    unittest.main()
