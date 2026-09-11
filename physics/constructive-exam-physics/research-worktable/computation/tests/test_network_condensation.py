import unittest

from sympy import Matrix, simplify, symbols

from occ.network import (
    LinearNetworkRequest,
    NetworkVariable,
    condense_linear_network,
)


def variable(symbol, physical_name, state_kind):
    return NetworkVariable(symbol, physical_name, state_kind)


def chain_request(area, state_kind, source=(0, 0, 0)):
    left, right, hidden = symbols("x_L x_R x_h")
    first, second = symbols("c_1 c_2", positive=True)
    return LinearNetworkRequest(
        area=area,
        variables=(
            variable(left, "left boundary state", state_kind),
            variable(right, "right boundary state", state_kind),
            variable(hidden, "hidden junction state", state_kind),
        ),
        boundary_symbols=(left, right),
        internal_symbols=(hidden,),
        response_matrix=(
            (first, 0, -first),
            (0, second, -second),
            (-first, -second, first + second),
        ),
        source_vector=source,
        provenance=f"{area} three-node chain bench",
    )


class NetworkCondensationTests(unittest.TestCase):
    def test_electrical_chain_constructs_exact_boundary_law_and_recovery(self):
        request = chain_request("electricity", "voltage")
        first, second = symbols("c_1 c_2", positive=True)
        left, right = request.boundary_symbols

        result = condense_linear_network(request)

        equivalent = first * second / (first + second)
        self.assertEqual(result.status, "constructed")
        self.assertEqual(
            Matrix(result.condensed_matrix),
            Matrix([[equivalent, -equivalent], [-equivalent, equivalent]]),
        )
        self.assertEqual(result.condensed_source, (0, 0))
        self.assertEqual(
            result.reconstruct_internal((left, right)),
            ((first * left + second * right) / (first + second),),
        )
        self.assertTrue(all(item.passed for item in result.certificates))

    def test_unchanged_constructor_transfers_to_spring_and_thermal_networks(self):
        spring = condense_linear_network(chain_request("mechanics", "displacement"))
        heat = symbols("Q")
        thermal_request = chain_request(
            "thermal physics", "temperature", source=(0, 0, heat)
        )
        thermal = condense_linear_network(thermal_request)
        first, second = symbols("c_1 c_2", positive=True)
        left, right = thermal_request.boundary_symbols

        self.assertEqual(spring.status, "constructed")
        self.assertEqual(thermal.status, "constructed")
        self.assertEqual(
            thermal.condensed_source,
            (first * heat / (first + second), second * heat / (first + second)),
        )
        recovered = thermal.reconstruct_internal((left, right))[0]
        self.assertEqual(
            simplify(
                recovered - (first * left + second * right + heat) / (first + second)
            ),
            0,
        )
        self.assertEqual(thermal.area, "thermal physics")
        self.assertEqual(thermal.state_kind, "temperature")
        self.assertIn("thermal physics", thermal.provenance)

    def test_two_hidden_states_are_condensed_without_preencoded_series_formula(self):
        left, first_hidden, second_hidden, right = symbols("x_0 x_1 x_2 x_3")
        first, second, third = symbols("c_1 c_2 c_3", positive=True)
        request = LinearNetworkRequest(
            area="electricity",
            variables=(
                variable(left, "left terminal voltage", "voltage"),
                variable(first_hidden, "first junction voltage", "voltage"),
                variable(second_hidden, "second junction voltage", "voltage"),
                variable(right, "right terminal voltage", "voltage"),
            ),
            boundary_symbols=(left, right),
            internal_symbols=(first_hidden, second_hidden),
            response_matrix=(
                (first, -first, 0, 0),
                (-first, first + second, -second, 0),
                (0, -second, second + third, -third),
                (0, 0, -third, third),
            ),
            source_vector=(0, 0, 0, 0),
            provenance="four-node conductance chain bench",
        )

        result = condense_linear_network(request)

        denominator = first * second + first * third + second * third
        equivalent = first * second * third / denominator
        self.assertEqual(
            Matrix(result.condensed_matrix),
            Matrix([[equivalent, -equivalent], [-equivalent, equivalent]]),
        )
        self.assertEqual(
            result.reconstruct_internal((1, 0)),
            (first * (second + third) / denominator, first * second / denominator),
        )
        self.assertTrue(all(item.passed for item in result.certificates))

    def test_singular_internal_block_is_a_typed_refusal(self):
        boundary, hidden = symbols("x_B x_h")
        request = LinearNetworkRequest(
            area="mechanics",
            variables=(
                variable(boundary, "boundary displacement", "displacement"),
                variable(hidden, "free hidden displacement", "displacement"),
            ),
            boundary_symbols=(boundary,),
            internal_symbols=(hidden,),
            response_matrix=((1, 0), (0, 0)),
            source_vector=(0, 0),
            provenance="singular free-mode bench",
        )

        result = condense_linear_network(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "internal_block_singular")
        self.assertEqual(result.condensed_matrix, ())

    def test_undetermined_internal_invertibility_is_not_assumed(self):
        boundary, hidden, coefficient = symbols("x_B x_h c")
        request = LinearNetworkRequest(
            area="generic linear response",
            variables=(
                variable(boundary, "boundary state", "potential"),
                variable(hidden, "hidden state", "potential"),
            ),
            boundary_symbols=(boundary,),
            internal_symbols=(hidden,),
            response_matrix=((1, 0), (0, coefficient)),
            source_vector=(0, 0),
            provenance="symbolic invertibility bench",
        )

        result = condense_linear_network(request)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "internal_invertibility_undetermined")

    def test_partition_must_cover_each_declared_variable_once(self):
        request = chain_request("electricity", "voltage")

        with self.assertRaisesRegex(ValueError, "partition"):
            condense_linear_network(
                LinearNetworkRequest(
                    area=request.area,
                    variables=request.variables,
                    boundary_symbols=request.boundary_symbols,
                    internal_symbols=(),
                    response_matrix=request.response_matrix,
                    source_vector=request.source_vector,
                    provenance=request.provenance,
                )
            )

    def test_budget_refuses_before_partial_elimination(self):
        request = chain_request("mechanics", "displacement")

        result = condense_linear_network(request, max_internal=0)

        self.assertEqual(result.status, "refused")
        self.assertEqual(result.obstruction.code, "internal_budget_exceeded")
        self.assertEqual(result.condensed_matrix, ())

    def test_no_internal_state_is_reported_as_irreducible(self):
        boundary = symbols("x_B")
        request = LinearNetworkRequest(
            area="electricity",
            variables=(variable(boundary, "terminal voltage", "voltage"),),
            boundary_symbols=(boundary,),
            internal_symbols=(),
            response_matrix=((2,),),
            source_vector=(3,),
            provenance="one-terminal bench",
        )

        result = condense_linear_network(request)

        self.assertEqual(result.status, "irreducible")
        self.assertEqual(result.obstruction.code, "no_internal_variables")
        self.assertEqual(result.condensed_matrix, ((2,),))
        self.assertEqual(result.condensed_source, (3,))


if __name__ == "__main__":
    unittest.main()
