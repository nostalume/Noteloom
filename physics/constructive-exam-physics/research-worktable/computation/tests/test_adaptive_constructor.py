import unittest

from sympy import sin, symbols

from occ.adaptive import (
    AdaptiveRelationRequest,
    construct_target_relation,
)
from occ.problem import PhysicalLaw


def law(name, relation, provenance="test theorem contract"):
    return PhysicalLaw(name, relation, provenance)


class AdaptiveConstructorTests(unittest.TestCase):
    def test_selects_smallest_target_path_from_unordered_laws_and_distractors(self):
        given, hidden, carrier, target, noise = symbols(
            "given hidden carrier target noise"
        )
        request = AdaptiveRelationRequest(
            problem_id="unseen-chain",
            laws=(
                law("distractor", noise - given),
                law("target readout", target - 3 * carrier),
                law("first transport", hidden - 2 * given),
                law("second transport", carrier - hidden),
                law("second distractor", noise**2 - 1),
            ),
            givens=(given,),
            target=target,
        )

        result = construct_target_relation(request)

        self.assertEqual(result.status, "constructed")
        self.assertEqual(
            {item.name for item in result.selected_laws},
            {"target readout", "first transport", "second transport"},
        )
        self.assertTrue(result.elimination.implies(target - 6 * given))

    def test_detects_competing_minimal_explanations(self):
        given, target = symbols("given target")
        request = AdaptiveRelationRequest(
            problem_id="ambiguous-input",
            laws=(
                law("route one", target - given),
                law("route two", target - 2 * given),
            ),
            givens=(given,),
            target=target,
        )

        result = construct_target_relation(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "ambiguous_minimal_packets")
        self.assertEqual(
            set(result.candidate_packets),
            {("route one",), ("route two",)},
        )

    def test_reports_when_no_supplied_law_mentions_the_target(self):
        given, hidden, target = symbols("given hidden target")
        request = AdaptiveRelationRequest(
            problem_id="missing-law",
            laws=(law("known relation", hidden - given),),
            givens=(given,),
            target=target,
        )

        result = construct_target_relation(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "no_target_path")

    def test_reports_connected_but_underdetermined_target(self):
        given, hidden, target = symbols("given hidden target")
        request = AdaptiveRelationRequest(
            problem_id="free-hidden-state",
            laws=(law("coupled law", target - hidden - given),),
            givens=(given,),
            target=target,
        )

        result = construct_target_relation(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "target_not_constrained")

    def test_reports_target_component_disconnected_from_all_givens(self):
        given, hidden, target = symbols("given hidden target")
        request = AdaptiveRelationRequest(
            problem_id="disconnected-data",
            laws=(
                law("target component", target - hidden),
                law("given component", given**2 - 1),
            ),
            givens=(given,),
            target=target,
        )

        result = construct_target_relation(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "disconnected_target")

    def test_reports_when_law_count_budget_prevents_closure(self):
        given, first, second, target = symbols("given first second target")
        request = AdaptiveRelationRequest(
            problem_id="bounded-chain",
            laws=(
                law("first", first - given),
                law("second", second - first),
                law("third", target - second),
            ),
            givens=(given,),
            target=target,
            max_selected_laws=2,
        )

        result = construct_target_relation(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "search_budget_exceeded")

    def test_equivalent_minimal_packets_are_not_physical_ambiguity(self):
        given, target = symbols("given target")
        request = AdaptiveRelationRequest(
            problem_id="equivalent-inputs",
            laws=(
                law("normalized", target - given),
                law("scaled", 2 * target - 2 * given),
            ),
            givens=(given,),
            target=target,
        )

        result = construct_target_relation(request)

        self.assertEqual(result.status, "constructed")
        self.assertEqual(len(result.candidate_packets), 2)
        self.assertTrue(result.elimination.implies(target - given))

    def test_a617_water_jet_transfer_ignores_cross_domain_distractors(self):
        impact, launch, gravity, height, alpha, density, area, mass = symbols(
            "impact launch gravity height alpha density area mass"
        )
        capacitance, voltage, charge, energy = symbols(
            "capacitance voltage charge energy"
        )
        laws = (
            law(
                "capacitor distractor",
                charge - capacitance * voltage,
                "parallel-plate capacitor contract",
            ),
            law(
                "momentum flux",
                (2 - alpha) * density * area * launch * impact - mass * gravity,
                "A617 page 29: absorbed plus reflected water momentum",
            ),
            law(
                "atomic distractor",
                2 * energy + mass,
                "unrelated spectral contract",
            ),
            law(
                "ballistic speed",
                impact**2 - launch**2 + 2 * gravity * height,
                "A617 page 29: energy along the rising jet",
            ),
        )
        request = AdaptiveRelationRequest(
            problem_id="A13-02-unlabeled-transfer",
            laws=laws,
            givens=(launch, gravity, alpha, density, area, mass),
            target=height,
        )

        result = construct_target_relation(request)

        expected = (2 - alpha) ** 2 * density**2 * area**2 * launch**2 * (
            launch**2 - 2 * gravity * height
        ) - mass**2 * gravity**2
        self.assertEqual(result.status, "constructed")
        self.assertEqual(
            {item.name for item in result.selected_laws},
            {"momentum flux", "ballistic speed"},
        )
        self.assertEqual(result.attempted_subsets, 3)
        self.assertTrue(result.elimination.implies(expected))

    def test_nonpolynomial_input_reports_backend_boundary(self):
        given, target = symbols("given target")
        request = AdaptiveRelationRequest(
            problem_id="transcendental",
            laws=(law("phase law", target - sin(given)),),
            givens=(given,),
            target=target,
        )

        result = construct_target_relation(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "unsupported_relation_shape")


if __name__ == "__main__":
    unittest.main()
