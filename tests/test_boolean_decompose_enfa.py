import numpy as np
import pytest
from pyformlang.finite_automaton import (
    State,
    EpsilonNFA,
    Symbol,
)
from scipy.sparse import coo_matrix

from project.automata_utils import (
    boolean_decompose_enfa,
)
from project.boolean_decomposition import BooleanDecomposition
from test_utils import create_automata

testdata = [
    (
        boolean_decompose_enfa(
            create_automata(
                transitions=[(0, "a", 0)],
                start_states=[0],
                final_states=[0],
                automata=EpsilonNFA(),
            )
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
    (
        boolean_decompose_enfa(
            create_automata(
                transitions=[(0, "a", 1)],
                start_states=[0],
                final_states=[1],
                automata=EpsilonNFA(),
            )
        ),
        BooleanDecomposition(
            {
                Symbol("a"): coo_matrix(
                    (np.array([1]), (np.array([0]), np.array([1]))), shape=(2, 2)
                )
            },
            [State(0), State(1)],
        ),
    ),
    (
        boolean_decompose_enfa(
            create_automata(
                transitions=[(0, "a", 1), (1, "b", 2)],
                start_states=[0],
                final_states=[2],
                automata=EpsilonNFA(),
            )
        ),
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
        ),
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_boolean_decompose_enfa(
    actual: BooleanDecomposition, expected: BooleanDecomposition
):
    assert actual == expected
