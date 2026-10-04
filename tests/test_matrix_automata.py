"""Check sparse automata against pyformlang and RPQ against explicit search."""

from collections import deque
from itertools import product
import random

import networkx as nx
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
import pytest
from scipy.sparse import csr_matrix

from project.automata_utils import graph_to_nfa, regex_to_dfa
from project.matrix_automata import AdjacencyMatrixFA, intersect_automata, tensor_based_rpq


def words(alphabet, max_length):
    for length in range(max_length + 1):
        yield from product(alphabet, repeat=length)


@pytest.mark.parametrize("regex", ["", "epsilon", "a", "a*", "(a | b)* a b", "token"])
def test_dfa_interpretation(regex):
    dfa = regex_to_dfa(regex)
    matrix_fa = AdjacencyMatrixFA(dfa)
    for word in words(["a", "b", "token", "unknown"], 3):
        assert matrix_fa.accepts(iter(word)) == dfa.accepts(word)
        assert matrix_fa.accepts(map(Symbol, word)) == dfa.accepts(word)
    assert matrix_fa.is_empty() == dfa.is_empty()


def test_nfa_multiple_starts_and_nondeterministic_transitions():
    nfa = NondeterministicFiniteAutomaton(states={State("isolated")})
    nfa.add_start_state("left")
    nfa.add_start_state("right")
    nfa.add_final_state("end")
    nfa.add_transitions(
        [
            ("left", "a", "dead"),
            ("left", "a", "middle"),
            ("middle", "b", "end"),
            ("right", "b", "end"),
        ]
    )
    matrix_fa = AdjacencyMatrixFA(nfa)
    assert matrix_fa.num_states == len(nfa.states)
    for matrix in matrix_fa.matrices.values():
        assert isinstance(matrix, csr_matrix)
        assert matrix.dtype == bool
        assert matrix.shape == (len(nfa.states), len(nfa.states))
    for word in words("ab", 4):
        assert matrix_fa.accepts(word) == nfa.accepts(word)
    assert not matrix_fa.is_empty()


def test_empty_and_isolated_automata():
    empty = AdjacencyMatrixFA(NondeterministicFiniteAutomaton())
    assert empty.num_states == 0
    assert empty.is_empty()
    assert not empty.accepts([])
    assert empty.transitive_closure().shape == (0, 0)

    nfa = NondeterministicFiniteAutomaton()
    nfa.add_start_state(10)
    nfa.add_final_state(20)
    matrix_fa = AdjacencyMatrixFA(nfa)
    assert matrix_fa.is_empty()
    assert not matrix_fa.accepts([])
    nfa.add_final_state(10)
    matrix_fa = AdjacencyMatrixFA(nfa)
    assert not matrix_fa.is_empty()
    assert matrix_fa.accepts([])
    assert not matrix_fa.accepts(["a"])


def test_transitive_closure_requires_multiple_squarings():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_start_state(0)
    nfa.add_final_state(12)
    for i in range(12):
        nfa.add_transition(i, "a" if i % 2 else "b", i + 1)
    matrix_fa = AdjacencyMatrixFA(nfa)
    closure = matrix_fa.transitive_closure()
    for source in range(13):
        for target in range(13):
            assert bool(
                closure[
                    matrix_fa.state_indices[State(source)],
                    matrix_fa.state_indices[State(target)],
                ]
            ) == (source <= target)
    assert not matrix_fa.is_empty()


@pytest.mark.parametrize(
    "left, right",
    [("a*", "b*"), ("a", "b"), ("(a | b)*", "a b*"), ("epsilon", "a*"), ("a b", "b a")],
)
def test_intersection_acceptance_and_rejection(left, right):
    fa1, fa2 = regex_to_dfa(left), regex_to_dfa(right)
    intersection = intersect_automata(AdjacencyMatrixFA(fa1), AdjacencyMatrixFA(fa2))
    for word in words("ab", 5):
        assert intersection.accepts(word) == (fa1.accepts(word) and fa2.accepts(word))
    assert intersection.is_empty() == fa1.get_intersection(fa2).is_empty()


def test_intersection_of_nfas_and_empty_automaton():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_start_state(10)
    nfa.add_start_state(20)
    nfa.add_final_state(30)
    nfa.add_transitions([(10, "a", 20), (10, "a", 30), (20, "b", 30)])
    matrix_fa = AdjacencyMatrixFA(nfa)
    intersection = intersect_automata(matrix_fa, matrix_fa)
    for word in words("ab", 4):
        assert intersection.accepts(word) == nfa.accepts(word)
    for left, right in [
        (AdjacencyMatrixFA(), matrix_fa),
        (matrix_fa, AdjacencyMatrixFA()),
    ]:
        intersection = intersect_automata(left, right)
        assert intersection.num_states == 0
        assert intersection.is_empty()
        assert not intersection.accepts([])


def test_rpq_parallel_edges_nonconsecutive_vertices_and_filters():
    graph = nx.MultiDiGraph()
    graph.add_nodes_from([10, 30, 90, -5])
    graph.add_edge(10, 30, label="a")
    graph.add_edge(10, 30, label="a")
    graph.add_edge(10, 30, label="b")
    graph.add_edge(30, 90, label="b")
    graph.add_edge(90, 90, label="b")
    assert tensor_based_rpq("a b*", graph) == {(10, 30), (10, 90)}
    assert tensor_based_rpq("a b*", graph, {10}, {90}) == {(10, 90)}
    assert tensor_based_rpq("a b*", graph, {30}, {90}) == set()
    assert tensor_based_rpq("epsilon", graph) == {(v, v) for v in graph}
    assert tensor_based_rpq("a*", graph, {10, -5}, {30, -5}) == {(10, 30), (-5, -5)}
    assert tensor_based_rpq("missing", graph) == set()


@pytest.mark.parametrize("regex", ["epsilon", "a", "a*"])
def test_rpq_empty_graph(regex):
    assert tensor_based_rpq(regex, nx.MultiDiGraph()) == set()


def reference_rpq(regex, graph, starts, finals):
    """An independent BFS over graph/DFA state pairs, without matrices."""
    dfa = regex_to_dfa(regex)
    result = set()
    for source in starts:
        visited = {(source, state) for state in dfa.start_states}
        queue = deque(visited)
        while queue:
            vertex, state = queue.popleft()
            if vertex in finals and state in dfa.final_states:
                result.add((source, vertex))
            for _, target, data in graph.out_edges(vertex, data=True):
                for next_state in dfa(state, data["label"]):
                    pair = (target, next_state)
                    if pair not in visited:
                        visited.add(pair)
                        queue.append(pair)
    return result


@pytest.mark.parametrize("seed", range(5))
def test_rpq_matches_explicit_product_search(seed):
    rng = random.Random(seed)
    graph = nx.MultiDiGraph()
    nodes = [-10, 20, 40, 100, 200]
    graph.add_nodes_from(nodes)
    for _ in range(15):
        graph.add_edge(
            rng.choice(nodes), rng.choice(nodes), label=rng.choice(["a", "b"])
        )
    starts, finals = set(nodes[:3]), set(nodes[2:])
    for regex in ["a", "a*", "a b", "(a | b)*", "(a b)*", "a* b a*", "epsilon"]:
        assert tensor_based_rpq(regex, graph, starts, finals) == reference_rpq(
            regex, graph, starts, finals
        )


def test_graph_conversion_preserves_isolated_vertices_and_inputs():
    graph = nx.MultiDiGraph()
    graph.add_nodes_from([10, 20, 30])
    graph.add_edge(10, 20, label="a")
    before = graph.copy()
    starts, finals = {10, 30}, {20, 30}
    nfa = graph_to_nfa(graph, starts, finals)
    assert {state.value for state in nfa.states} == {10, 20, 30}
    assert {state.value for state in nfa.start_states} == starts
    assert {state.value for state in nfa.final_states} == finals
    assert nfa.accepts([])
    assert nfa.accepts(["a"])
    assert nx.utils.graphs_equal(graph, before)
    assert starts == {10, 30} and finals == {20, 30}
    for boundaries in [(None, None), (set(), set())]:
        nfa = graph_to_nfa(graph, *boundaries)
        assert nfa.start_states == nfa.final_states == nfa.states
        assert tensor_based_rpq("epsilon", graph, *boundaries) == {
            (v, v) for v in graph
        }


def test_graph_conversion_rejects_unknown_boundary_vertices():
    graph = nx.MultiDiGraph()
    graph.add_node(10)
    with pytest.raises(ValueError, match="graph vertices"):
        graph_to_nfa(graph, {20}, {10})
