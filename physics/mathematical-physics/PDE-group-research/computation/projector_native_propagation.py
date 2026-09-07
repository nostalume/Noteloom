"""Lower coefficient-derived projector jets into invariant window propagation."""

from __future__ import annotations

from coefficient_projector_jet import SpectralProjectorJet
from finite_window_propagation import (
    FinitePropagationWindow,
    WindowPropagationWitness,
    construct_off_block_window_propagation,
)
from off_block_differential import construct_off_block_differential
from simple_block_pde import IrreducibleModel


def construct_projector_window_propagation(
    model: IrreducibleModel,
    projector_jet: SpectralProjectorJet,
    window: FinitePropagationWindow,
) -> WindowPropagationWitness:
    """Use the local Grassmann first/second arrows without choosing a moving frame."""
    differential = construct_off_block_differential(
        model,
        projector_jet.projector,
        projector_jet.first_off_block_operator,
        projector_jet.second_off_block_operator,
        "G14 coefficient-derived projector jet",
    )
    return construct_off_block_window_propagation(model, differential, window)
