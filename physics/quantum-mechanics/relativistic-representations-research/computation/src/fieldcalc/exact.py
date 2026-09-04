"""Exact finite-dimensional certificates delegated to SymPy domains."""

from dataclasses import dataclass

from sympy import Matrix


@dataclass(frozen=True)
class KernelCertificate:
    matrix: Matrix
    rank: int
    nullity: int
    basis: tuple[Matrix, ...]


def kernel_certificate(matrix: Matrix) -> KernelCertificate:
    admitted = Matrix(matrix)
    basis = tuple(admitted.nullspace())
    rank = admitted.rank()
    nullity = admitted.cols - rank
    if len(basis) != nullity:
        raise ArithmeticError("rank-nullity certificate failed")
    if any(admitted * vector != Matrix.zeros(admitted.rows, 1) for vector in basis):
        raise ArithmeticError("reported vector is not in the kernel")
    return KernelCertificate(admitted, rank, nullity, basis)
