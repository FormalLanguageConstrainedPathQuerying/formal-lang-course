import pytest
import cfpq_data
from networkx import MultiDiGraph
from project.rpq import rpq_tensors, rpq_bfs


def test_empty():
    empty_graph, empty_regex = MultiDiGraph(), ""
    graph, regex = MultiDiGraph([(0, 1, {"label": "a"})]), "a"

    assert rpq_tensors(empty_graph, [0], [1], empty_regex) == set()
    assert rpq_tensors(empty_graph, [0], [1], regex) == set()
    assert rpq_tensors(graph, [0], [1], empty_regex) == set()
    assert rpq_bfs(empty_graph, [0], [1], empty_regex) == set()
    assert rpq_bfs(empty_graph, [0], [1], regex) == set()
    assert rpq_bfs(graph, [0], [1], empty_regex) == set()
    assert rpq_bfs(empty_graph, [0], [1], empty_regex, group_by_start=True) == dict()
    assert rpq_bfs(empty_graph, [0], [1], regex, group_by_start=True) == dict()
    assert rpq_bfs(graph, [0], [1], empty_regex, group_by_start=True) == dict()


def test_no_start_final():
    graph = MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 0, {"label": "a"}),
            (0, 0, {"label": "a"}),
            (1, 1, {"label": "a"}),
        ]
    )
    regex = "a*"

    assert rpq_tensors(graph, [0, 1], [], regex) == set()
    assert rpq_tensors(graph, [], [0, 1], regex) == set()
    assert rpq_tensors(graph, [], [], regex) == set()
    assert rpq_bfs(graph, [0, 1], [], regex) == set()
    assert rpq_bfs(graph, [], [0, 1], regex) == set()
    assert rpq_bfs(graph, [], [], regex) == set()
    assert rpq_bfs(graph, [0, 1], [], regex, group_by_start=True) == dict()
    assert rpq_bfs(graph, [], [0, 1], regex, group_by_start=True) == dict()
    assert rpq_bfs(graph, [], [], regex, group_by_start=True) == dict()


def test_all_reachable():
    graph = cfpq_data.labeled_cycle_graph(5)
    regex = "a*"

    assert len(rpq_tensors(graph, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], regex)) == 25
    assert rpq_bfs(graph, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], regex) == {0, 1, 2, 3, 4}
    for reachable in rpq_bfs(
        graph, [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], regex, group_by_start=True
    ).values():
        assert reachable == {0, 1, 2, 3, 4}


@pytest.fixture()
def complex_graph() -> MultiDiGraph:
    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edges_from(
        [
            (0, 1, {"label": "k"}),
            (1, 2, {"label": "a"}),
            (2, 3, {"label": "b"}),
            (3, 4, {"label": "a"}),
            (4, 5, {"label": "n"}),
            (4, 7, {"label": "n"}),
            (4, 8, {"label": "n"}),
            (6, 1, {"label": "K"}),
        ]
    )

    return graph


@pytest.fixture()
def complex_regex() -> str:
    return "(K|k)a.b(a+$)n*"


def test_rpq_pairs_complex(complex_graph, complex_regex):
    reachable_pairs = rpq_tensors(
        complex_graph, [0, 6], [0, 1, 2, 3, 4, 5, 7], complex_regex
    )

    assert reachable_pairs == {
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 7),
        (6, 3),
        (6, 4),
        (6, 5),
        (6, 7),
    }


def test_rpq_all_reachable_complex(complex_graph, complex_regex):
    reachable = rpq_bfs(complex_graph, [0, 6], [0, 1, 2, 3, 4, 5, 7], complex_regex)

    assert reachable == {3, 4, 5, 7}


def test_rpq_grouped_reachable_complex(complex_graph, complex_regex):
    reachable = rpq_bfs(
        complex_graph, [0, 6], [0, 1, 2, 3, 4, 5, 7], complex_regex, group_by_start=True
    )

    assert reachable == {0: {3, 4, 5, 7}, 6: {3, 4, 5, 7}}
