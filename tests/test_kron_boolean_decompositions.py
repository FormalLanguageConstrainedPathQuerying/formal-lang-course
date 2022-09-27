import numpy as np
import pytest
from pyformlang.finite_automaton import (
    State,
    Symbol,
)
from scipy.sparse import coo_matrix

from project.automata_utils import (
    kron_boolean_decompositions,
)
from project.boolean_decomposition import BooleanDecomposition

testdata = [
    (
        kron_boolean_decompositions(
            BooleanDecomposition(
                {
                    Symbol("a"): coo_matrix(
                        (np.array([1]), (np.array([0]), np.array([0]))), shape=(1, 1)
                    )
                },
                [State(0)],
            ),
            BooleanDecomposition(
                {
                    Symbol("a"): coo_matrix(
                        (np.array([1]), (np.array([0]), np.array([0]))), shape=(1, 1)
                    )
                },
                [State(0)],
            ),
        ),
        BooleanDecomposition(
            {
                Symbol("a"): coo_matrix(
                    (np.array([1]), (np.array([0]), np.array([0]))), shape=(1, 1)
                )
            },
            [State((State(0), State(0)))],
        ),
    ),
    (
        kron_boolean_decompositions(
            BooleanDecomposition(
                {
                    Symbol("a"): coo_matrix(
                        (np.array([1]), (np.array([0]), np.array([0]))), shape=(1, 1)
                    )
                },
                [State(0)],
            ),
            BooleanDecomposition(
                {
                    Symbol("b"): coo_matrix(
                        (np.array([1]), (np.array([0]), np.array([0]))), shape=(1, 1)
                    )
                },
                [State(0)],
            ),
        ),
        BooleanDecomposition(
            {Symbol("a"): coo_matrix((1, 1)), Symbol("b"): coo_matrix((1, 1))},
            [State((State(0), State(0)))],
        ),
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_kron_boolean_decompositions(
    actual: BooleanDecomposition, expected: BooleanDecomposition
):
    assert actual == expected
