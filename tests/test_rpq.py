from collections import deque
from random import Random

import pytest
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.rpq import tensor_based_rpq


def _rpq_by_traversal(
    regex: str, graph: MultiDiGraph, starts: set[int], finals: set[int]
) -> set[tuple[int, int]]:
    """Evaluate paths with BFS over pairs of graph vertices and query states."""
    query = Regex(regex).to_epsilon_nfa().to_deterministic()
    allowed_starts = starts or set(graph.nodes)
    allowed_finals = finals or set(graph.nodes)
    result = set()

    for source in allowed_starts:
        visited = {(source, state) for state in query.start_states}
        queue = deque(visited)
        while queue:
            vertex, state = queue.popleft()
            if vertex in allowed_finals and state in query.final_states:
                result.add((source, vertex))
            for _, target, label in graph.out_edges(vertex, data="label"):
                for next_state in query(state, label):
                    pair = (target, next_state)
                    if pair not in visited:
                        visited.add(pair)
                        queue.append(pair)

    return result


@pytest.fixture
def path_graph():
    graph = MultiDiGraph()
    graph.add_nodes_from([100, -7, 42, 999])
    graph.add_edge(100, -7, label="a")
    graph.add_edge(-7, 42, label="b")
    return graph


@pytest.mark.parametrize(
    ("regex", "starts", "finals", "expected"),
    [
        pytest.param("a b", {100}, {42}, {(100, 42)}, id="original-vertex-identifiers"),
        pytest.param("a b", {-7}, {42}, set(), id="start-restriction"),
        pytest.param("a b", {100}, {-7}, set(), id="final-restriction"),
        pytest.param("b a", {100}, {42}, set(), id="label-order"),
        pytest.param("b a", {42}, {100}, set(), id="edge-direction"),
        pytest.param("a | b", set(), {42}, {(-7, 42)}, id="default-starts"),
        pytest.param("a | b", {100}, set(), {(100, -7)}, id="default-finals"),
        pytest.param(
            "a | b", set(), set(), {(100, -7), (-7, 42)}, id="default-both-endpoints"
        ),
        pytest.param(
            "epsilon",
            {100, 999},
            {42, 999},
            {(999, 999)},
            id="restricted-zero-length-paths",
        ),
        pytest.param(
            "missing*",
            {999},
            {999},
            {(999, 999)},
            id="isolated-vertex-and-absent-label",
        ),
        pytest.param(
            "a", {999}, {999}, set(), id="isolated-vertex-rejects-nonempty-word"
        ),
        pytest.param("", set(), set(), set(), id="empty-language"),
    ],
)
def test_tensor_rpq_paths(path_graph, regex, starts, finals, expected):
    assert tensor_based_rpq(regex, path_graph, starts, finals) == expected


@pytest.mark.parametrize(
    ("has_loop", "expected"),
    [
        pytest.param(True, {(100, 42)}, id="traverses-loop"),
        pytest.param(False, set(), id="rejects-shorter-path-without-loop"),
    ],
)
def test_tensor_rpq_requires_loop_for_last_symbol(path_graph, has_loop, expected):
    if has_loop:
        path_graph.add_edge(42, 42, label="b")

    assert tensor_based_rpq("a b b", path_graph, {100}, {42}) == expected


@pytest.mark.parametrize("label", ["a", "b"])
def test_tensor_rpq_preserves_parallel_edge_labels(label):
    graph = MultiDiGraph()
    graph.add_edge(10, 20, label="a")
    graph.add_edge(10, 20, label="a")
    graph.add_edge(10, 20, label="b")

    assert tensor_based_rpq(label, graph, {10}, {20}) == {(10, 20)}


def test_tensor_rpq_returns_all_reachable_endpoint_pairs():
    graph = MultiDiGraph()
    graph.add_edge(10, 30, label="a")
    graph.add_edge(20, 30, label="a")
    graph.add_edge(20, 40, label="a")

    result = tensor_based_rpq("a", graph, {10, 20}, {30, 40})

    assert result == {(10, 30), (20, 30), (20, 40)}


def test_tensor_rpq_uses_all_accepting_regex_states(path_graph):
    result = tensor_based_rpq("a | a b", path_graph, {100}, {-7, 42})

    assert result == {(100, -7), (100, 42)}


def test_tensor_rpq_empty_graph():
    assert tensor_based_rpq("a*", MultiDiGraph(), set(), set()) == set()


@pytest.mark.parametrize(
    ("starts", "finals"),
    [
        pytest.param({1234}, {42}, id="unknown-start"),
        pytest.param({100}, {1234}, id="unknown-final"),
    ],
)
def test_tensor_rpq_rejects_unknown_vertices(path_graph, starts, finals):
    with pytest.raises(ValueError, match="vertices"):
        tensor_based_rpq("a*", path_graph, starts, finals)


def test_tensor_rpq_multicharacter_labels():
    graph = MultiDiGraph()
    graph.add_edge(10, 20, label="first")
    graph.add_edge(20, 30, label="second")

    assert tensor_based_rpq("first second", graph, {10}, {30}) == {(10, 30)}


def test_tensor_rpq_does_not_modify_inputs(path_graph):
    before = path_graph.copy()
    starts, finals = {100}, {42}

    tensor_based_rpq("a b*", path_graph, starts, finals)

    assert dict(path_graph.nodes(data=True)) == dict(before.nodes(data=True))
    assert list(path_graph.edges(keys=True, data=True)) == list(
        before.edges(keys=True, data=True)
    )
    assert starts == {100}
    assert finals == {42}


@pytest.mark.parametrize("seed", range(12))
@pytest.mark.parametrize(
    "regex",
    [
        pytest.param("a b", id="concatenation"),
        pytest.param("a | b", id="alternative"),
        pytest.param("a*", id="repetition"),
        pytest.param("(a b)*", id="repeated-sequence"),
        pytest.param("a (b | c)*", id="alternative-in-repetition"),
    ],
)
def test_tensor_rpq_matches_traversal_on_generated_graphs(seed, regex):
    rng = Random(seed)
    nodes = [-10, 8, 42, 100]
    graph = MultiDiGraph()
    graph.add_nodes_from(nodes)
    for source in nodes:
        for target in nodes:
            for label in ["a", "b", "c"]:
                if rng.random() < 0.25:
                    graph.add_edge(source, target, label=label)
    starts = {node for node in nodes if rng.random() < 0.5}
    finals = {node for node in nodes if rng.random() < 0.5}
    expected = _rpq_by_traversal(regex, graph, starts, finals)

    assert tensor_based_rpq(regex, graph, starts, finals) == expected, (
        seed,
        regex,
        starts,
        finals,
        list(graph.edges(data="label")),
    )
