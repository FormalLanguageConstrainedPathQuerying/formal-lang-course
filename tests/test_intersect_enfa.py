import pytest
from pyformlang.finite_automaton import EpsilonNFA

from project.automata_utils import intersect_enfa
from test_utils import create_automata

testdata = [
    (
        intersect_enfa(
            create_automata(
                transitions=[(0, "a", 0)],
                start_states=[0],
                final_states=[0],
                automata=EpsilonNFA(),
            ),
            create_automata(
                transitions=[(0, "a", 0)],
                start_states=[0],
                final_states=[0],
                automata=EpsilonNFA(),
            ),
        ),
        create_automata(
            transitions=[(0, "a", 0)],
            start_states=[0],
            final_states=[0],
            automata=EpsilonNFA(),
        ),
    ),
    (
        intersect_enfa(
            create_automata(
                transitions=[(0, "a", 0)],
                start_states=[0],
                final_states=[0],
                automata=EpsilonNFA(),
            ),
            create_automata(
                transitions=[(0, "b", 0)],
                start_states=[0],
                final_states=[0],
                automata=EpsilonNFA(),
            ),
        ),
        create_automata(
            transitions=[], start_states=[0], final_states=[0], automata=EpsilonNFA()
        ),
    ),
    (
        intersect_enfa(
            create_automata(
                transitions=[(0, "a", 0)],
                start_states=[0],
                final_states=[0],
                automata=EpsilonNFA(),
            ),
            create_automata(
                transitions=[(0, "a", 1), (1, "b", 2)],
                start_states=[0],
                final_states=[1, 2],
                automata=EpsilonNFA(),
            ),
        ),
        create_automata(
            transitions=[(0, "a", 1)],
            start_states=[0],
            final_states=[1],
            automata=EpsilonNFA(),
        ),
    ),
    (
        intersect_enfa(
            create_automata(
                transitions=[(0, "a", 1), (0, "b", 2)],
                start_states=[0],
                final_states=[1, 2],
                automata=EpsilonNFA(),
            ),
            create_automata(
                transitions=[(0, "a", 1), (0, "b", 2), (1, "a", 1), (2, "b", 2)],
                start_states=[0],
                final_states=[1, 2],
                automata=EpsilonNFA(),
            ),
        ),
        create_automata(
            transitions=[(0, "a", 1), (0, "b", 2)],
            start_states=[0],
            final_states=[1, 2],
            automata=EpsilonNFA(),
        ),
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_intersect_enfa(actual: EpsilonNFA, expected: EpsilonNFA):
    assert actual.is_equivalent_to(expected)
