import unittest

from sympy import Rational, pi, simplify, sqrt, symbols

from occ.path import (
    ParameterizedPath,
    PathFunctionalRequest,
    PlanarVectorField,
    construct_path_functionals,
    construct_two_path_circuit,
    resolve_free_space_potential_difference,
    resolve_open_wire_voltage,
)
from worktable.path_cases import build_a10_case, build_a14_case, run_path_transfer


class PathFunctionalTests(unittest.TestCase):
    def test_a14_constructs_arc_chord_functionals_and_two_branch_circuit(self):
        case = build_a14_case()

        result = construct_path_functionals(case.request)
        circuit = construct_two_path_circuit(
            result,
            "minor arc",
            "straight chord",
            case.parameters["rho"],
        )

        a = case.parameters["a"]
        kappa = case.parameters["kappa"]
        rho = case.parameters["rho"]
        arc = result.path("minor arc")
        chord = result.path("straight chord")
        self.assertEqual(result.status, "constructed")
        self.assertEqual(simplify(arc.line_work - pi * kappa * a**2), 0)
        self.assertEqual(simplify(chord.line_work - 2 * kappa * a**2), 0)
        self.assertEqual(simplify(arc.length - pi * a / 2 ** Rational(1, 2)), 0)
        self.assertEqual(chord.length, 2 * a)
        self.assertEqual(
            simplify(
                result.work_difference("minor arc", "straight chord")
                - kappa * a**2 * (pi - 2)
            ),
            0,
        )
        self.assertEqual(
            simplify(
                result.signed_area_difference("minor arc", "straight chord")
                + a**2 * (pi / 2 - 1)
            ),
            0,
        )
        self.assertEqual(result.curl, -2 * kappa)
        self.assertTrue(
            any(
                certificate.name == "constant_curl_path_difference"
                and certificate.passed
                for certificate in result.certificates
            )
        )
        self.assertEqual(circuit.status, "constructed")
        expected_voltage = simplify(
            (arc.line_work * rho * chord.length + chord.line_work * rho * arc.length)
            / (rho * (arc.length + chord.length))
        )
        self.assertEqual(simplify(circuit.terminal_voltage - expected_voltage), 0)
        self.assertEqual(
            simplify(
                circuit.terminal_voltage
                - 2 * pi * kappa * a**2 * (sqrt(2) + 1) / (pi + 2 * sqrt(2))
            ),
            0,
        )
        self.assertEqual(
            simplify(
                circuit.first_current
                - sqrt(2) * kappa * a * (pi - 2) / (rho * (pi + 2 * sqrt(2)))
            ),
            0,
        )
        expected_current = simplify(
            (arc.line_work - chord.line_work) / (rho * (arc.length + chord.length))
        )
        self.assertEqual(simplify(circuit.first_current - expected_current), 0)
        self.assertEqual(simplify(circuit.second_current + circuit.first_current), 0)
        self.assertTrue(all(certificate.passed for certificate in circuit.certificates))

    def test_constant_curl_recovers_every_pair_in_a_three_path_batch(self):
        x, y, t, c = symbols("x y t c", real=True)
        field = PlanarVectorField(
            "constant curl field",
            coordinates=(x, y),
            components=(0, c * x),
            parameters=(c,),
            provenance="fixture",
        )
        paths = (
            ParameterizedPath("straight", t, 0, 1, (t, 0), "fixture"),
            ParameterizedPath("upper", t, 0, 1, (t, t * (1 - t)), "fixture"),
            ParameterizedPath("lower", t, 0, 1, (t, -t * (1 - t)), "fixture"),
        )

        result = construct_path_functionals(
            PathFunctionalRequest(field, paths, max_paths=3)
        )

        self.assertEqual(result.status, "constructed")
        names = tuple(path.name for path in paths)
        for index, first in enumerate(names):
            for second in names[index + 1 :]:
                self.assertEqual(
                    simplify(
                        result.work_difference(first, second)
                        - c * result.signed_area_difference(first, second)
                    ),
                    0,
                )
        self.assertTrue(
            any(
                certificate.name == "constant_curl_path_difference"
                and certificate.passed
                for certificate in result.certificates
            )
        )

    def test_a10_transfers_unchanged_and_refuses_path_free_endpoint_voltage(self):
        case = build_a10_case()

        result = construct_path_functionals(case.request)

        radius = case.parameters["radius"]
        kappa = case.parameters["kappa"]
        self.assertEqual(
            simplify(result.path("short arc").line_work + pi * kappa * radius**2 / 2),
            0,
        )
        self.assertEqual(
            simplify(
                result.path("long arc").line_work - 3 * pi * kappa * radius**2 / 2
            ),
            0,
        )
        self.assertEqual(
            resolve_open_wire_voltage(result, "short arc").status,
            "constructed",
        )
        free_space = resolve_free_space_potential_difference(result)
        self.assertEqual(free_space.status, "refused")
        self.assertEqual(free_space.obstruction.code, "no_scalar_potential_certificate")

    def test_path_reversal_negates_work_and_preserves_length(self):
        x, y, t = symbols("x y t")
        field = PlanarVectorField(
            "constant field",
            coordinates=(x, y),
            components=(1, 2),
            parameters=(),
            provenance="fixture",
        )
        path = ParameterizedPath(
            "forward",
            parameter=t,
            lower=0,
            upper=1,
            position=(t, t**2),
            provenance="fixture",
        )

        forward = construct_path_functionals(PathFunctionalRequest(field, (path,)))
        reverse = construct_path_functionals(
            PathFunctionalRequest(field, (path.reversed("reverse"),))
        )

        self.assertEqual(
            simplify(
                forward.path("forward").line_work + reverse.path("reverse").line_work
            ),
            0,
        )
        self.assertEqual(
            simplify(forward.path("forward").length - reverse.path("reverse").length),
            0,
        )

    def test_verified_scalar_potential_recovers_path_independent_endpoint_value(self):
        x, y, t = symbols("x y t")
        field = PlanarVectorField(
            "conservative field",
            coordinates=(x, y),
            components=(-1, -1),
            parameters=(),
            provenance="fixture",
            scalar_potential=x + y,
        )
        paths = (
            ParameterizedPath("diagonal", t, 0, 1, (t, t), "fixture"),
            ParameterizedPath("curved", t, 0, 1, (t, t**2), "fixture"),
        )

        result = construct_path_functionals(PathFunctionalRequest(field, paths))
        endpoint = resolve_free_space_potential_difference(result)

        self.assertEqual(result.status, "constructed")
        self.assertEqual(endpoint.status, "constructed")
        self.assertEqual(endpoint.value, 2)
        self.assertTrue(all(path.line_work == -2 for path in result.paths))

    def test_paths_with_different_orientated_endpoints_are_refused(self):
        x, y, t = symbols("x y t")
        field = PlanarVectorField("constant field", (x, y), (1, 0), (), "fixture")
        paths = (
            ParameterizedPath("first", t, 0, 1, (t, 0), "fixture"),
            ParameterizedPath("second", t, 0, 1, (0, t), "fixture"),
        )

        result = construct_path_functionals(PathFunctionalRequest(field, paths))

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "endpoint_mismatch")

    def test_source_transfer_artifact_runs_both_problems_without_interface_change(self):
        transfer = run_path_transfer()

        self.assertEqual(transfer.construction.status, "constructed")
        self.assertEqual(transfer.transfer.status, "constructed")
        self.assertEqual(transfer.free_space_voltage.status, "refused")


if __name__ == "__main__":
    unittest.main()
