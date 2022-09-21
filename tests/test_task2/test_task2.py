import filecmp

import cfpq_data
import networkx
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    EpsilonNFA,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import Regex

from project.regex_utils import (
    regex_to_dfa,
    create_automaton,
    create_graph,
    create_nfa_from_graph,
)


def to_string(automaton):
    return networkx.drawing.nx_pydot.to_pydot(automaton.to_networkx()).to_string()


def test_regex_to_graph_one_letter():
    dfa = regex_to_dfa(Regex("a"))
    expected = create_automaton(
        transitions=[(0, "a", 1)],
        start_states=[0],
        final_states=[1],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert dfa.is_equivalent_to(expected)


def test_regex_to_graph_long_lable():
    dfa = regex_to_dfa(Regex("long_lable"))
    expected = create_automaton(
        transitions=[(0, "long_lable", 1)],
        start_states=[0],
        final_states=[1],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert dfa.is_equivalent_to(expected)


def test_regex_to_graph_two_letter():
    dfa = regex_to_dfa(Regex("a b"))
    expected = create_automaton(
        transitions=[(0, "a", 1), (1, "b", 2)],
        start_states=[0],
        final_states=[2],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert dfa.is_equivalent_to(expected)


def test_regex_to_graph_loop():
    dfa = regex_to_dfa(Regex("a*"))
    expected = create_automaton(
        transitions=[(0, "a", 0)],
        start_states=[0],
        final_states=[0],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert dfa.is_equivalent_to(expected)


def test_create_nfa_from_graph_two_gen_cycle(tmp_path):
    graph = cfpq_data.labeled_two_cycles_graph(3, 2, labels=["a", "a"])
    automaton = create_nfa_from_graph(graph, start_states=[0], final_states=[2, 5])

    path_of_expected = tmp_path / "tmp.dot"
    with open(path_of_expected, "w") as f:
        f.write(to_string(automaton))

    assert filecmp.cmp("./tests/test_task2/expected_cyc.dot", path_of_expected)


def test_create_nfa_from_graph():
    automaton = create_nfa_from_graph(
        graph=create_graph([0, 1, 2], [(0, "a", 1), (0, "a", 2)]),
        start_states={0},
        final_states={1, 2},
    )

    expected = create_automaton(
        transitions=[(0, "a", 1), (0, "a", 2)],
        start_states=[0],
        final_states=[1, 2],
        automaton=EpsilonNFA(),
    )

    assert to_string(automaton) == to_string(expected)


def test_create_nfa_from_empty():
    automaton: NondeterministicFiniteAutomaton = create_nfa_from_graph(
        graph=create_graph([], [])
    )

    expected = create_automaton(
        transitions=[],
        start_states=[],
        final_states=[],
        automaton=NondeterministicFiniteAutomaton(),
    )

    assert to_string(automaton) == to_string(expected)


def test_regex_to_graph_one_empty():
    dfa = regex_to_dfa(Regex(""))
    expected = create_automaton(
        transitions=[],
        start_states=[],
        final_states=[],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert to_string(dfa) == to_string(expected)


def test_create_nfa_from_graph_1():
    automaton = create_nfa_from_graph(
        graph=create_graph(
            [0, 1, 2, 3],
            [
                (0, "a", 1),
                (0, "a", 2),
                (1, "b", 2),
                (2, "b", 3),
                (3, "b", 0),
                (1, "b", 1),
            ],
        ),
        start_states={0},
        final_states={1, 3},
    )

    expected = create_automaton(
        transitions=[
            (0, "a", 1),
            (0, "a", 2),
            (1, "b", 2),
            (2, "b", 3),
            (3, "b", 0),
            (1, "b", 1),
        ],
        start_states=[0],
        final_states=[1, 3],
        automaton=EpsilonNFA(),
    )

    assert to_string(automaton) == to_string(expected)


def test_create_nfa_from_graph_2():
    automaton = create_nfa_from_graph(
        graph=create_graph([0, 1, 2, 3], []),
        start_states={0},
        final_states={1, 3},
    )

    expected = create_automaton(
        transitions=[],
        start_states=[0],
        final_states=[1, 3],
        automaton=EpsilonNFA(),
    )

    assert to_string(automaton) == to_string(expected)


def test_create_nfa_from_graph_3():
    automaton = create_nfa_from_graph(
        graph=create_graph(
            [0, 1, 2, 3],
            [
                (0, "a", 0),
                (0, "a", 1),
                (0, "a", 2),
                (0, "a", 3),
                (1, "a", 0),
                (1, "a", 1),
                (1, "a", 2),
                (1, "a", 3),
                (2, "a", 0),
                (2, "a", 1),
                (2, "a", 2),
                (2, "a", 3),
                (3, "a", 0),
                (3, "a", 1),
                (3, "a", 2),
                (3, "a", 3),
            ],
        ),
    )

    expected = create_automaton(
        transitions=[
            (0, "a", 0),
            (0, "a", 1),
            (0, "a", 2),
            (0, "a", 3),
            (1, "a", 0),
            (1, "a", 1),
            (1, "a", 2),
            (1, "a", 3),
            (2, "a", 0),
            (2, "a", 1),
            (2, "a", 2),
            (2, "a", 3),
            (3, "a", 0),
            (3, "a", 1),
            (3, "a", 2),
            (3, "a", 3),
        ],
        start_states=[0, 1, 2, 3],
        final_states=[0, 1, 2, 3],
        automaton=EpsilonNFA(),
    )

    assert to_string(automaton) == to_string(expected)
