from pyformlang.finite_automaton import (
    Symbol,
    State,
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from project.graph_utils import get_graph_info, create_two_cycles_graph
from project.fa_utils import regex2dfa, graph2nfa
import pytest
import random
import cfpq_data


def test_rege2dfa_correct():
    regex = "a b"
    test = regex2dfa(regex)

    state_0 = State(0)
    state_1 = State(1)
    state_2 = State(2)
    a = Symbol("a")
    b = Symbol("b")

    expect = DeterministicFiniteAutomaton()
    expect.add_start_state(state_0)
    expect.add_final_state(state_2)

    expect.add_transition(state_0, a, state_1)
    expect.add_transition(state_1, b, state_2)

    assert test.is_equivalent_to(expect)


def test_regex2dfa_minimal():
    letters = "abcdefghklmnopqrstuvwxyz "

    for _ in range(10):
        left = ""
        for _ in range(random.randint(2, 10)):
            left += letters[random.randint(0, len(letters) - 1)]
        right = ""
        for _ in range(random.randint(2, 10)):
            right += letters[random.randint(0, len(letters) - 1)]

        if random.randint(0, 1) == 1:
            left += "*"
        if random.randint(0, 1) == 1:
            right += "*"
        if random.randint(0, 1) == 1:
            right = right + "*"

        if random.randint(0, 1) == 1:
            regex = f"{left}|{right}"
        else:
            regex = f"{left}{right}"

        dfa = regex2dfa(regex)
        assert dfa.is_deterministic()
        minimal = dfa.minimize()
        assert dfa.is_equivalent_to(minimal)
        assert len(minimal.states) == len(dfa.states)
        assert minimal.get_number_transitions() == dfa.get_number_transitions()


def test_graph2nfa_named():

    names = ["wc", "bzip", "pr", "ls", "gzip", "biomedical", "pathways"]

    for name in names:
        fa = graph2nfa(cfpq_data.graph_from_csv(cfpq_data.download(name)))
        graph_info = get_graph_info(name)

        assert fa.symbols == graph_info["unique_labels"]
        assert len(fa.start_states) == graph_info["number_of_nodes"]
        assert len(fa.final_states) == graph_info["number_of_nodes"]


def test_nfa_from_two_cycle_graph_building():

    for _ in range(10):

        n = random.randint(1, 10)
        m = random.randint(1, 10)

        graph = create_two_cycles_graph((n, m), ("a", "b"), "/tmp/two_cycles")
        fa = graph2nfa(graph)

        assert fa.symbols == {"a", "b"}
        assert fa.accepts(["a", "a"])
        assert fa.accepts(["a", "b"])
        assert fa.accepts(["b", "a"])
        assert fa.accepts(["b", "b"])

        assert len(fa.start_states) == n + m + 1
        assert len(fa.final_states) == n + m + 1
