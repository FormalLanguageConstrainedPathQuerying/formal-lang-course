import pytest

from project.automata_tools import regex_to_minimal_dfa, graph_to_nfa
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    State,
    Symbol,
)
import filecmp
import os
import cfpq_data
from project.graph_tools import load_graph

task_2_tests_dir_path = os.path.dirname(os.path.abspath(__file__))


def test_empty_regex_to_minimal_dfa():
    regex = Regex("")
    min_dfa = regex_to_minimal_dfa(regex)
    assert min_dfa.is_empty()


def test_regex_to_minimal_dfa():
    regex = Regex("(0|1 0)*")

    expected_dfa = DeterministicFiniteAutomaton()

    state_1 = State(1)
    state_2 = State(2)

    zero = Symbol("0")
    one = Symbol("1")

    expected_dfa.add_start_state(state_1)
    expected_dfa.add_final_state(state_1)

    expected_dfa.add_transition(state_1, zero, state_1)
    expected_dfa.add_transition(state_1, one, state_2)
    expected_dfa.add_transition(state_2, zero, state_1)

    actual_dfa = regex_to_minimal_dfa(regex)

    assert expected_dfa.is_equivalent_to(actual_dfa)


# @pytest.mark.parametrize("dataset_graph_name", ["atom", "wine", "pizza"])
# def test_dataset_graph_to_nfa(dataset_graph_name):
#     graph = load_graph(dataset_graph_name)
#     nfa = graph_to_nfa(graph, start_states=None, final_states=None)
#
#     assert len(nfa.final_states) == len(graph.nodes)
#     assert len(nfa.start_states) == len(graph.nodes)


def test_graph_to_nfa_without_start_and_final_states():
    graph = cfpq_data.labeled_two_cycles_graph(3, 7, labels=("a1", "a2"))
    nfa = graph_to_nfa(graph, start_states=None, final_states=None)
    nfa.write_as_dot("actual_two_cycle_graph_without_start_and_final_states.dot")

    assert filecmp.cmp(
        "actual_two_cycle_graph_without_start_and_final_states.dot",
        os.sep.join(
            [
                task_2_tests_dir_path,
                "expected/two_cycle_graph_without_start_and_final_states.dot",
            ]
        ),
    )
    os.remove("actual_two_cycle_graph_without_start_and_final_states.dot")


def test_graph_to_nfa():
    graph = cfpq_data.labeled_two_cycles_graph(2, 3, labels=("a1", "a2"))
    nfa = graph_to_nfa(graph, start_states={0}, final_states={1, 3, 5})
    nfa.write_as_dot("actual_cycles_graph.dot")

    assert filecmp.cmp(
        "actual_cycles_graph.dot",
        os.sep.join([task_2_tests_dir_path, "expected/two_cycles_graph.dot"]),
    )
    os.remove("actual_cycles_graph.dot")
