from dataclasses import replace
import unittest

from sympy import I, Matrix, Rational, eye, simplify, sqrt, symbols, zeros

from fieldcalc.departure import DepartureRequest, FockState, MatterBosonVertex, compile_departure
from fieldcalc.instrument import VisibleInstrumentRequest, compile_visible_instrument


class DepartureCompilerTests(unittest.TestCase):
    def setUp(self):
        vacuum = (0, 0, 0)
        self.preparations = (
            FockState("e0", vacuum),
            FockState("e1", vacuum),
        )
        self.channels = tuple(
            FockState("g", tuple(1 if index == mode else 0 for index in range(3)))
            for mode in range(3)
        )
        self.vertices = (
            MatterBosonVertex("e0", "g", 0, "create", Rational(1, 2), "v0"),
            MatterBosonVertex("e0", "g", 2, "create", Rational(1, 3), "v1"),
            MatterBosonVertex("e1", "g", 0, "create", Rational(1, 5), "v2"),
            MatterBosonVertex("e1", "g", 1, "create", Rational(1, 4), "v3"),
            MatterBosonVertex("e1", "g", 2, "create", Rational(-1, 6), "v4"),
        )
        self.request = DepartureRequest(
            preparations=self.preparations,
            channels=self.channels,
            vertices=self.vertices,
            provenance="two-level three-mode action jet",
            resource_budget=32,
        )

    def test_action_terms_generate_departure_before_contraction(self):
        result = compile_departure(self.request)
        self.assertTrue(result.accepted)
        self.assertEqual(result.departure, Matrix([
            [Rational(1, 2), Rational(1, 5)],
            [0, Rational(1, 4)],
            [Rational(1, 3), Rational(-1, 6)],
        ]))
        self.assertEqual(result.bose_factors, (1, 1, 1, 1, 1))
        self.assertEqual(result.applied_origins, ("v0", "v1", "v2", "v3", "v4"))
        self.assertEqual(result.resource_cost, 16)
        self.assertTrue(result.closed)

    def test_generated_departure_feeds_bound_and_detector_routes(self):
        compiled = compile_departure(self.request)
        departure = compiled.departure
        left = Matrix.diag(1, 0, 0)
        rest = Matrix.diag(0, 1, 1)
        visible = compile_visible_instrument(VisibleInstrumentRequest(
            departure=departure,
            effects={"left": left, "rest": rest},
            partition=("left", "rest"),
            provenance="same finite Hamiltonian composition bench",
            resource_budget=32,
        )).instrument
        retained_hamiltonian = Matrix.diag(-2, -1)
        channel_hamiltonian = Matrix.diag(0, 1, 2)
        full_hamiltonian = (
            retained_hamiltonian.row_join(departure.H)
            .col_join(departure.row_join(channel_hamiltonian))
        )
        spectral_parameter = symbols("z")
        channel_resolvent = (
            spectral_parameter * eye(3) - channel_hamiltonian
        ).inv()
        denominator = (
            spectral_parameter * eye(2)
            - retained_hamiltonian
            - visible.compress(channel_resolvent).value
        )
        determinant_residual = simplify(
            (spectral_parameter * eye(5) - full_hamiltonian).det()
            - (spectral_parameter * eye(3) - channel_hamiltonian).det()
            * denominator.det()
        )
        self.assertEqual(determinant_residual, 0)
        off_axis = I
        channel_resolvent = (off_axis * eye(3) - channel_hamiltonian).inv()
        denominator = (
            off_axis * eye(2)
            - retained_hamiltonian
            - visible.compress(channel_resolvent).value
        )
        predicted_qp = channel_resolvent * departure * denominator.inv()
        full_resolvent = (off_axis * eye(5) - full_hamiltonian).inv()
        direct_qp = full_resolvent[2:5, 0:2]
        self.assertEqual((direct_qp - predicted_qp).applyfunc(simplify), zeros(3, 2))
        preparation = Matrix([1, 1])
        direct = simplify((direct_qp * preparation).H * left * direct_qp * preparation)
        compressed_detector = visible.compress(channel_resolvent.H * left * channel_resolvent)
        predicted = simplify(
            preparation.H * denominator.inv().H
            * compressed_detector.value * denominator.inv() * preparation
        )
        self.assertEqual(simplify(direct[0] - predicted[0]), 0)

    def test_occupied_sector_transfers_creation_and_annihilation(self):
        create, annihilate = symbols("g_c g_a")
        result = compile_departure(DepartureRequest(
            preparations=(FockState("e", (1, 1)),),
            channels=(FockState("g", (2, 1)), FockState("g", (0, 1))),
            vertices=(
                MatterBosonVertex("e", "g", 0, "create", create, "creation"),
                MatterBosonVertex("e", "g", 0, "annihilate", annihilate, "annihilation"),
            ),
            provenance="occupied-sector transfer",
            resource_budget=8,
        ))
        self.assertTrue(result.accepted)
        self.assertEqual(result.departure, Matrix([[sqrt(2) * create], [annihilate]]))
        self.assertEqual(result.bose_factors, (sqrt(2), 1))

    def test_incomplete_channel_duplicate_basis_invalid_mode_and_budget_are_refused(self):
        requests = (
            (
                replace(self.request, channels=self.channels[:2]),
                "channel basis omits a generated state",
            ),
            (
                replace(
                    self.request,
                    preparations=(self.preparations[0], self.preparations[0]),
                ),
                "preparation basis contains duplicates",
            ),
            (
                replace(
                    self.request,
                    vertices=(MatterBosonVertex(
                        "e0", "g", 4, "create", 1, "bad mode",
                    ),),
                ),
                "vertex mode lies outside the occupation basis",
            ),
            (
                replace(
                    self.request,
                    vertices=(MatterBosonVertex(
                        "e0", "g", 0, "rotate", 1, "bad action",
                    ),),
                ),
                "vertex action is not supported",
            ),
            (
                replace(
                    self.request,
                    preparations=(FockState("e", (0,)),),
                    channels=(FockState("g", (1, 0)),),
                ),
                "occupation tuples have inconsistent lengths",
            ),
            (
                replace(
                    self.request,
                    vertices=(MatterBosonVertex(
                        "absent", "g", 0, "create", 1, "unused",
                    ),),
                ),
                "interaction generates no departure",
            ),
            (
                replace(self.request, resource_budget=1),
                "departure compilation budget exceeded",
            ),
        )

        for request, reason in requests:
            with self.subTest(reason=reason):
                result = compile_departure(request)
                self.assertFalse(result.accepted)
                self.assertEqual(result.refusal.reason, reason)
if __name__ == "__main__":
    unittest.main()
