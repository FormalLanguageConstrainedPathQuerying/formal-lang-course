from collections.abc import Hashable, Iterable
from copy import deepcopy
from itertools import product
from random import Random

import pytest
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from scipy.sparse import issparse

from project.adjacency_matrix_fa import AdjacencyMatrixFA, intersect_automata
from project.automata_utils import regex_to_dfa


def _make_nfa(
    transitions: Iterable[tuple[Hashable, str, Hashable]] = (),
    starts: Iterable[Hashable] = (),
    finals: Iterable[Hashable] = (),
    states: Iterable[Hashable] = (),
) -> NondeterministicFiniteAutomaton:
    """Build an NFA with explicit transitions and endpoint sets."""
    nfa = NondeterministicFiniteAutomaton(states=set(states))
    nfa.add_transitions(transitions)
    for state in starts:
        nfa.add_start_state(state)
    for state in finals:
        nfa.add_final_state(state)
    return nfa


def _matrix_transitions(
    automaton: AdjacencyMatrixFA,
) -> set[tuple[Hashable, Hashable, Hashable]]:
    """Decode transitions and check that all matrices use the declared state space."""
    transitions = set()
    for symbol, matrix in automaton.matrices.items():
        assert issparse(matrix), f"Matrix for {symbol} must be sparse"
        assert matrix.dtype == bool, f"Matrix for {symbol} must be boolean"
        assert matrix.shape == (len(automaton.states), len(automaton.states)), symbol
        for row, column in zip(*matrix.nonzero()):
            transitions.add(
                (
                    automaton.states[row].value,
                    symbol.value,
                    automaton.states[column].value,
                )
            )
    return transitions


@pytest.fixture
def branching_nfa():
    return _make_nfa(
        [("s", "a", 10), ("s", "a", 20), (10, "b", "f"), (20, "c", "f")],
        starts=["s"],
        finals=["f"],
        states=[("isolated", 0)],
    )


def test_constructor_preserves_isolated_states(branching_nfa):
    matrix_fa = AdjacencyMatrixFA(branching_nfa)

    assert set(matrix_fa.states) == {
        State(s) for s in ["s", 10, 20, "f", ("isolated", 0)]
    }


def test_constructor_preserves_labeled_transitions_in_boolean_sparse_matrices(
    branching_nfa,
):
    matrix_fa = AdjacencyMatrixFA(branching_nfa)

    actual = _matrix_transitions(matrix_fa)
    assert actual == {("s", "a", 10), ("s", "a", 20), (10, "b", "f"), (20, "c", "f")}


def test_constructor_language_is_independent_of_source_changes():
    nfa = _make_nfa([(0, "a", 1)], starts=[0], finals=[1])
    matrix_fa = AdjacencyMatrixFA(nfa)

    # Replace the source language {a} with b* using new states and transitions.
    nfa.remove_transition(0, "a", 1)
    nfa.remove_start_state(0)
    nfa.remove_final_state(1)
    nfa.add_transition(2, "b", 2)
    nfa.add_start_state(2)
    nfa.add_final_state(2)

    assert matrix_fa.accepts(["a"])
    assert not matrix_fa.accepts(["b"])
    assert not matrix_fa.accepts([])


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        pytest.param(("a", "b"), True, id="first-nondeterministic-branch"),
        pytest.param(("a", "c"), True, id="second-nondeterministic-branch"),
        pytest.param((), False, id="empty-word-with-distinct-endpoints"),
        pytest.param(("a",), False, id="nonfinal-prefix"),
        pytest.param(("a", "b", "c"), False, id="extra-symbol"),
        pytest.param(("b", "a"), False, id="wrong-order"),
        pytest.param(("x",), False, id="unknown-symbol"),
        pytest.param(("a", "a"), False, id="known-symbol-with-no-transition"),
    ],
)
def test_accepts_nondeterministic_words(branching_nfa, word, expected):
    assert AdjacencyMatrixFA(branching_nfa).accepts(word) is expected


def test_accepts_symbol_iterator_with_multicharacter_label():
    matrix_fa = AdjacencyMatrixFA(regex_to_dfa("label other"))

    assert matrix_fa.accepts(Symbol(label) for label in ["label", "other"])


def test_accepts_does_not_split_multicharacter_symbols():
    assert not AdjacencyMatrixFA(regex_to_dfa("label")).accepts("label")


@pytest.mark.parametrize(
    ("starts", "finals", "transitions", "expected"),
    [
        pytest.param([], [1], [(0, "a", 1)], True, id="no-starts"),
        pytest.param([0], [], [(0, "a", 1)], True, id="no-finals"),
        pytest.param([0], [1], [], True, id="disconnected-isolated-states"),
        pytest.param([0], [0], [], False, id="epsilon-only"),
        pytest.param([0], [1], [(0, "a", 1)], False, id="one-transition"),
        pytest.param([1], [0], [(0, "a", 1)], True, id="opposite-direction"),
        pytest.param(
            [0], [2], [(0, "a", 1), (1, "b", 0)], True, id="nonaccepting-cycle"
        ),
        pytest.param([0, 1], [2, 3], [(1, "a", 3)], False, id="multiple-endpoints"),
    ],
)
def test_is_empty_checks_reachability(starts, finals, transitions, expected):
    matrix_fa = AdjacencyMatrixFA(_make_nfa(transitions, starts, finals))

    assert matrix_fa.is_empty() is expected


def test_empty_automaton_rejects_empty_word():
    matrix_fa = AdjacencyMatrixFA(NondeterministicFiniteAutomaton())

    assert not matrix_fa.accepts(())


def test_empty_automaton_has_empty_language():
    matrix_fa = AdjacencyMatrixFA(NondeterministicFiniteAutomaton())

    assert matrix_fa.is_empty()


def test_closure_of_empty_automaton():
    matrix_fa = AdjacencyMatrixFA(NondeterministicFiniteAutomaton())

    closure = matrix_fa.transitive_closure()

    assert issparse(closure)
    assert closure.dtype == bool
    assert closure.shape == (0, 0)


def test_closure_includes_long_directed_paths_and_zero_length_paths():
    matrix_fa = AdjacencyMatrixFA(_make_nfa([(i, "a", i + 1) for i in range(9)]))

    closure = matrix_fa.transitive_closure()
    reachable = {
        (matrix_fa.states[i].value, matrix_fa.states[j].value)
        for i, j in zip(*closure.nonzero())
    }

    assert issparse(closure)
    assert closure.dtype == bool
    assert reachable == {(i, j) for i in range(10) for j in range(i, 10)}


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        pytest.param((), True, id="shared-empty-word"),
        pytest.param(("b", "b", "b"), True, id="shared-symbol"),
        pytest.param(("a",), False, id="left-only-symbol"),
        pytest.param(("c",), False, id="right-only-symbol"),
        pytest.param(("b", "a"), False, id="word-outside-intersection"),
    ],
)
def test_intersection_language(word, expected):
    left = AdjacencyMatrixFA(regex_to_dfa("(a | b)*"))
    right = AdjacencyMatrixFA(regex_to_dfa("(b | c)*"))

    assert intersect_automata(left, right).accepts(word) is expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        pytest.param("a", "b", True, id="disjoint-alphabets"),
        pytest.param("a b", "b a", True, id="same-alphabet-incompatible-order"),
        pytest.param("epsilon", "a", True, id="only-one-accepts-empty-word"),
        pytest.param("a*", "b*", False, id="only-empty-word-in-common"),
    ],
)
def test_intersection_emptiness(left, right, expected):
    result = intersect_automata(
        AdjacencyMatrixFA(regex_to_dfa(left)), AdjacencyMatrixFA(regex_to_dfa(right))
    )

    assert result.is_empty() is expected


@pytest.mark.parametrize(
    "empty_first", [True, False], ids=["left-empty", "right-empty"]
)
def test_intersection_with_no_states_has_empty_language(empty_first):
    empty = AdjacencyMatrixFA(NondeterministicFiniteAutomaton())
    nonempty = AdjacencyMatrixFA(regex_to_dfa("a*"))
    left, right = (empty, nonempty) if empty_first else (nonempty, empty)

    result = intersect_automata(left, right)

    assert result.is_empty()


def test_intersection_does_not_modify_inputs():
    left = AdjacencyMatrixFA(regex_to_dfa("a b*"))
    right = AdjacencyMatrixFA(regex_to_dfa("a* | b"))
    before = deepcopy((left, right))

    intersect_automata(left, right)

    for actual, expected in zip((left, right), before):
        assert actual.states == expected.states
        assert actual.start_states == expected.start_states
        assert actual.final_states == expected.final_states
        assert actual.matrices.keys() == expected.matrices.keys()
        for symbol in expected.matrices:
            assert (actual.matrices[symbol] != expected.matrices[symbol]).nnz == 0


def test_intersection_state_pairs_match_their_transitions():
    left = AdjacencyMatrixFA(
        _make_nfa([(10, "a", 20), (10, "b", 30)], starts=[10], finals=[20, 30])
    )
    right = AdjacencyMatrixFA(
        _make_nfa([("s", "a", "f"), ("s", "c", "s")], starts=["s"], finals=["f"])
    )

    intersection = intersect_automata(left, right)

    assert {intersection.states[i].value for i in intersection.start_states} == {
        (10, "s")
    }
    assert {intersection.states[i].value for i in intersection.final_states} == {
        (20, "f"),
        (30, "f"),
    }
    assert _matrix_transitions(intersection) == {((10, "s"), "a", (20, "f"))}


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        pytest.param((), False, id="rejects-empty-word"),
        pytest.param(("b",), True, id="accepts-common-word"),
        pytest.param(("b", "b"), False, id="rejects-repetition"),
    ],
)
def test_intersection_can_be_intersected_again(word, expected):
    first = intersect_automata(
        AdjacencyMatrixFA(regex_to_dfa("a | b")),
        AdjacencyMatrixFA(regex_to_dfa("b | c")),
    )

    result = intersect_automata(first, AdjacencyMatrixFA(regex_to_dfa("b*")))

    assert result.accepts(word) == expected


def _random_nfa(rng: Random) -> NondeterministicFiniteAutomaton:
    """Generate a small NFA with independently chosen transitions and endpoints."""
    states = range(rng.randrange(1, 6))
    return _make_nfa(
        [
            (s, label, t)
            for s, label, t in product(states, "ab", states)
            if rng.random() < 0.25
        ],
        starts=[s for s in states if rng.random() < 0.5],
        finals=[s for s in states if rng.random() < 0.5],
        states=states,
    )


def _describe_nfa(nfa: NondeterministicFiniteAutomaton) -> str:
    """Include endpoints as well as transitions in generated test failures."""
    return (
        f"states={nfa.states}, starts={nfa.start_states}, "
        f"finals={nfa.final_states}, transitions={nfa.to_dict()}"
    )


@pytest.mark.parametrize("seed", range(12))
def test_matrix_acceptance_matches_nfa_on_generated_inputs(seed):
    nfa = _random_nfa(Random(seed))
    matrix_fa = AdjacencyMatrixFA(nfa)

    for length in range(5):
        for word in product("ab", repeat=length):
            assert matrix_fa.accepts(word) == nfa.accepts(word), (
                seed,
                word,
                _describe_nfa(nfa),
            )


@pytest.mark.parametrize("seed", range(12))
def test_matrix_emptiness_matches_nfa_on_generated_inputs(seed):
    nfa = _random_nfa(Random(seed))

    assert AdjacencyMatrixFA(nfa).is_empty() == nfa.is_empty(), (
        seed,
        _describe_nfa(nfa),
    )


@pytest.mark.parametrize("seed", range(12))
def test_intersection_acceptance_matches_both_nfas_on_generated_inputs(seed):
    rng = Random(seed)
    left, right = _random_nfa(rng), _random_nfa(rng)
    result = intersect_automata(AdjacencyMatrixFA(left), AdjacencyMatrixFA(right))

    for length in range(5):
        for word in product("ab", repeat=length):
            expected = left.accepts(word) and right.accepts(word)
            assert result.accepts(word) == expected, (
                seed,
                word,
                _describe_nfa(left),
                _describe_nfa(right),
            )


@pytest.mark.parametrize("seed", range(12))
def test_intersection_emptiness_matches_nfas_on_generated_inputs(seed):
    rng = Random(seed)
    left, right = _random_nfa(rng), _random_nfa(rng)
    result = intersect_automata(AdjacencyMatrixFA(left), AdjacencyMatrixFA(right))

    assert result.is_empty() == left.get_intersection(right).is_empty(), (
        seed,
        _describe_nfa(left),
        _describe_nfa(right),
    )
