from fractions import Fraction
import unittest

from sympy import symbols

from occ.semantic import (
    Dimension,
    PhysicalRelationPacket,
    QuantitySemantics,
    compile_single_source_functional,
)


ZERO = Dimension(0, 0, 0, 0)
LENGTH = Dimension(0, 1, 0, 0)
VELOCITY = Dimension(0, 1, -1, 0)
POWER = Dimension(1, 2, -3, 0)
ELECTRIC_DISPLACEMENT = Dimension(0, -2, 1, 1)
ELECTRIC_FIELD = Dimension(1, 1, -3, -1)
VOLTAGE = Dimension(1, 2, -3, -1)
CURRENT_RATE = Dimension(0, 0, -1, 1)


def quantity(symbol, name, dimension, *required_features):
    return QuantitySemantics(
        symbol=symbol,
        physical_name=name,
        dimension=dimension,
        required_features=frozenset(required_features),
    )


class SemanticLayerCompilerTests(unittest.TestCase):
    def test_dielectric_extracts_linear_source_field_functional(self):
        displacement, field_1, field_2, voltage = symbols("D E_1 E_2 U")
        packet = PhysicalRelationPacket(
            area="electromagnetism/dielectric",
            source=quantity(
                displacement,
                "electric displacement",
                ELECTRIC_DISPLACEMENT,
            ),
            fields=(
                quantity(field_1, "electric field sample 1", ELECTRIC_FIELD),
                quantity(field_2, "electric field sample 2", ELECTRIC_FIELD),
            ),
            target=quantity(voltage, "potential difference", VOLTAGE, "signed"),
            relations=(
                field_1 - displacement,
                field_2 - 2 * displacement,
                voltage - field_1 - field_2,
            ),
            map_coefficient_dimension=ELECTRIC_FIELD - ELECTRIC_DISPLACEMENT,
            functional_weight_dimension=LENGTH,
            regime=("planar symmetry", "positive permittivity"),
            conventions=("voltage orientation fixed",),
        )

        result = compile_single_source_functional(packet)

        self.assertEqual(result.status, "compiled")
        self.assertEqual(result.skeleton.functional_kind, "linear")
        self.assertEqual(result.skeleton.field_map, ((Fraction(1),), (Fraction(2),)))
        self.assertEqual(result.target_relation.expand(), voltage - 3 * displacement)
        self.assertEqual(result.ledger.area, "electromagnetism/dielectric")
        self.assertIn("voltage orientation fixed", result.ledger.conventions)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_conducting_rod_extracts_quadratic_heating(self):
        current_rate, field_1, field_2, power = symbols("s E_1 E_2 P")
        packet = PhysicalRelationPacket(
            area="electromagnetism/induction",
            source=quantity(current_rate, "current rate", CURRENT_RATE),
            fields=(
                quantity(field_1, "azimuthal field sample 1", ELECTRIC_FIELD),
                quantity(field_2, "azimuthal field sample 2", ELECTRIC_FIELD),
            ),
            target=quantity(power, "Joule power", POWER, "magnitude"),
            relations=(
                field_1 - current_rate,
                field_2 - 2 * current_rate,
                power - field_1**2 - 3 * field_2**2,
            ),
            map_coefficient_dimension=ELECTRIC_FIELD - CURRENT_RATE,
            functional_weight_dimension=POWER - 2 * ELECTRIC_FIELD,
            regime=("quasistatic induction", "Ohmic conductor"),
            conventions=("instantaneous power",),
        )

        result = compile_single_source_functional(packet)

        self.assertEqual(result.status, "compiled")
        self.assertEqual(result.skeleton.functional_kind, "quadratic")
        self.assertEqual(result.target_relation.expand(), power - 13 * current_rate**2)
        self.assertTrue(all(certificate.passed for certificate in result.certificates))

    def test_unseen_mechanical_dissipation_reuses_the_quadratic_skeleton(self):
        speed, damper_1, damper_2, power = symbols("v v_1 v_2 P")
        packet = PhysicalRelationPacket(
            area="mechanics/viscous-dissipation",
            source=quantity(speed, "driving speed", VELOCITY),
            fields=(
                quantity(damper_1, "damper speed 1", VELOCITY),
                quantity(damper_2, "damper speed 2", VELOCITY),
            ),
            target=quantity(power, "dissipated power", POWER, "magnitude"),
            relations=(
                damper_1 - 2 * speed,
                damper_2 + speed,
                power - 3 * damper_1**2 - 5 * damper_2**2,
            ),
            map_coefficient_dimension=ZERO,
            functional_weight_dimension=Dimension(1, 0, -1, 0),
            regime=("linear viscous damping",),
            conventions=("positive dissipation",),
        )

        result = compile_single_source_functional(packet)

        self.assertEqual(result.status, "compiled")
        self.assertEqual(result.skeleton.field_map, ((Fraction(2),), (Fraction(-1),)))
        self.assertEqual(result.target_relation.expand(), power - 17 * speed**2)
        self.assertEqual(result.ledger.area, "mechanics/viscous-dissipation")

    def test_phase_dependent_target_refuses_after_quadratic_extraction(self):
        source, field, torque = symbols("u f tau")
        packet = PhysicalRelationPacket(
            area="electromagnetism/rotating-coil",
            source=quantity(source, "EMF amplitude", ZERO),
            fields=(quantity(field, "current magnitude", ZERO),),
            target=quantity(torque, "instantaneous torque", ZERO, "phase"),
            relations=(field - source, torque - field**2),
            map_coefficient_dimension=ZERO,
            functional_weight_dimension=ZERO,
            regime=("steady harmonic response",),
            conventions=("instantaneous target",),
        )

        result = compile_single_source_functional(packet)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "semantic_feature_lost")
        self.assertIn("phase", result.obstruction.message)

    def test_dimensionally_invalid_return_is_refused(self):
        source, field, target = symbols("u f o")
        packet = PhysicalRelationPacket(
            area="invalid-fixture",
            source=quantity(source, "speed", VELOCITY),
            fields=(quantity(field, "speed", VELOCITY),),
            target=quantity(target, "mis-typed target", VOLTAGE, "magnitude"),
            relations=(field - source, target - field**2),
            map_coefficient_dimension=ZERO,
            functional_weight_dimension=Dimension(1, 0, -1, 0),
            regime=(),
            conventions=(),
        )

        result = compile_single_source_functional(packet)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "dimension_mismatch")

    def test_field_budget_refuses_before_extraction(self):
        source, field_1, field_2, target = symbols("u f_1 f_2 o")
        packet = PhysicalRelationPacket(
            area="budget-fixture",
            source=quantity(source, "source", ZERO),
            fields=(
                quantity(field_1, "field 1", ZERO),
                quantity(field_2, "field 2", ZERO),
            ),
            target=quantity(target, "target", ZERO, "signed"),
            relations=(field_1 - source, field_2 - source, target - field_1 - field_2),
            map_coefficient_dimension=ZERO,
            functional_weight_dimension=ZERO,
            regime=(),
            conventions=(),
        )

        result = compile_single_source_functional(packet, max_fields=1)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "field_budget_exceeded")

    def test_nonlinear_source_to_field_map_refuses_this_extraction_layer(self):
        source, field, target = symbols("u f o")
        packet = PhysicalRelationPacket(
            area="nonlinear-fixture",
            source=quantity(source, "source", ZERO),
            fields=(quantity(field, "field", ZERO),),
            target=quantity(target, "target", ZERO, "signed"),
            relations=(field - source**2, target - field),
            map_coefficient_dimension=ZERO,
            functional_weight_dimension=ZERO,
            regime=(),
            conventions=(),
        )

        result = compile_single_source_functional(packet)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "unsupported_relation_shape")


if __name__ == "__main__":
    unittest.main()
