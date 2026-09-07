from __future__ import annotations

import unittest
from fractions import Fraction

from natural_relation_planner import (
    METRIC_SEED_CAPABILITY,
    plan_tensor_relations,
    quotient_audit,
)
from tensor_seed_compression import (
    CovariantTensor,
    SlotQuotient,
    SymmetricPowerQuotient,
    TensorQuotient,
)


def tensor(
    name: str,
    rank: int,
    *,
    generators: tuple[tuple[int, ...], ...],
    capabilities: frozenset[str] = frozenset(),
    certificate: str | None = "constructed test relation",
    quotient: TensorQuotient | None = None,
) -> CovariantTensor:
    dimension = 3
    components = tuple(
        Fraction(1 if rank == 2 and index % 4 == 0 else 0) for index in range(dimension**rank)
    )
    return CovariantTensor(
        name=name,
        dimension=dimension,
        rank=rank,
        components=components,
        permutation_generators=generators,
        capabilities=capabilities,
        relation_certificate=certificate,
        quotient=quotient,
    )


def metric(name: str = "anonymous-form") -> CovariantTensor:
    return tensor(
        name,
        2,
        generators=((1, 0),),
        capabilities=frozenset({METRIC_SEED_CAPABILITY}),
        quotient=SymmetricPowerQuotient(SlotQuotient(), 2),
    )


class NaturalRelationPlannerTests(unittest.TestCase):
    def test_generic_permutation_generators_construct_the_route(self) -> None:
        relations = (
            metric(),
            tensor(
                "anonymous-four-tensor",
                4,
                generators=((1, 0, 2, 3), (0, 1, 3, 2), (2, 3, 0, 1)),
                quotient=SymmetricPowerQuotient(SymmetricPowerQuotient(SlotQuotient(), 2), 2),
            ),
        )

        first = plan_tensor_relations(relations)
        second = plan_tensor_relations(relations)
        structured = first.routes[1]

        self.assertEqual(first, second)
        self.assertEqual(first.preferred_route, "natural-tensor-structured-seed")
        self.assertEqual(structured.outcome, "planned")
        self.assertEqual([target.dimension for target in structured.targets], [21])
        self.assertEqual(structured.estimated_cost, 117)
        self.assertEqual(structured.planning_cost, 21)
        self.assertEqual(structured.estimated_total_cost, 138)
        self.assertEqual(
            [operation.rule for operation in structured.operations],
            [
                "metric-kernel",
                "compositional-quotient",
                "simultaneous-defect-kernel",
                "visible-quotient",
                "bracket-closure",
            ],
        )
        self.assertEqual(quotient_audit(structured), (True, 648))

    def test_undeclared_permutation_rejects_only_structured_plan(self) -> None:
        planning = plan_tensor_relations(
            (metric(), tensor("uncertified-four-tensor", 4, generators=(), certificate=None))
        )

        raw, structured = planning.routes
        self.assertEqual(raw.outcome, "planned")
        self.assertEqual(structured.outcome, "rejected")
        self.assertEqual(structured.obstruction_kind, "MissingQuotientConstructor")
        self.assertEqual(planning.preferred_route, "natural-tensor-raw-endomorphism")

    def test_multiple_seed_capabilities_are_not_ordered_arbitrarily(self) -> None:
        planning = plan_tensor_relations((metric("form-a"), metric("form-b")))

        structured = planning.routes[1]
        self.assertEqual(structured.outcome, "rejected")
        self.assertEqual(structured.obstruction_kind, "AmbiguousSeedRelation")
        self.assertEqual(planning.preferred_route, "natural-tensor-raw-endomorphism")

    def test_missing_seed_capability_preserves_only_the_raw_plan(self) -> None:
        planning = plan_tensor_relations((tensor("plain-two-tensor", 2, generators=((1, 0),)),))

        structured = planning.routes[1]
        self.assertEqual(structured.outcome, "rejected")
        self.assertEqual(structured.obstruction_kind, "MissingSeedRelation")
        self.assertEqual(planning.preferred_route, "natural-tensor-raw-endomorphism")


if __name__ == "__main__":
    unittest.main()
