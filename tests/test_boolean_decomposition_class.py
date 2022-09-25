import numpy as np
import pytest
from pyformlang.finite_automaton import (
    State,
    EpsilonNFA,
    Symbol,
)
from scipy.sparse import coo_matrix

from project.automata_utils import (
    BooleanDecomposition,
    boolean_decompose_enfa,
)
from test_utils import create_automata

testdata = [
    (
        BooleanDecomposition(
            {
                Symbol("a"): coo_matrix(
                    (np.array([1]), (np.array([0]), np.array([0]))), shape=(1, 1)
                )
            },
            [State(0)],
        ).transitive_closure(),
        coo_matrix((np.array([1]), (np.array([0]), np.array([0]))), shape=(1, 1)),
    ),
    (
        BooleanDecomposition(
            {
                Symbol("a"): coo_matrix(
                    (np.array([1]), (np.array([0]), np.array([1]))), shape=(2, 2)
                ),
                Symbol("b"): coo_matrix(
                    (np.array([1]), (np.array([1]), np.array([1]))), shape=(2, 2)
                ),
            },
            [State(0), State(1)],
        ).transitive_closure(),
        coo_matrix(
            (np.array([1, 1]), (np.array([0, 1]), np.array([1, 1]))), shape=(2, 2)
        ),
    ),
    (
        BooleanDecomposition(
            {
                Symbol("a"): coo_matrix(
                    (np.array([1]), (np.array([0]), np.array([1]))), shape=(3, 3)
                ),
                Symbol("b"): coo_matrix(
                    (np.array([1]), (np.array([1]), np.array([2]))), shape=(3, 3)
                ),
            },
            [State(0), State(1), State(2)],
        ).transitive_closure(),
        coo_matrix(
            (np.array([1, 1, 1]), (np.array([0, 1, 0]), np.array([1, 2, 2]))),
            shape=(3, 3),
        ),
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_boolean_decomposition_transitive_closure(
    actual: coo_matrix, expected: coo_matrix
):
    nonzero_actual = set(zip(*actual.nonzero()))
    nonzero_expected = set(zip(*expected.nonzero()))
    assert nonzero_actual == nonzero_expected
