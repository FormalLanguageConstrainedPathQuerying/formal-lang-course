import pytest
from networkx import MultiDiGraph
from project.rpq import rpq_tensors, rpq_bfs


@pytest.fixture()
def graph() -> MultiDiGraph:
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
def regex() -> str:
    return "(K|k)a.b(a+$)n*"


def test_rpq_pairs(graph, regex):
    reachable_pairs = rpq_tensors(graph, [0, 6], [0, 1, 2, 3, 4, 5, 7], regex)

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


def test_rpq_all_reachable(graph, regex):
    reachable = rpq_bfs(graph, [0, 6], [0, 1, 2, 3, 4, 5, 7], regex)

    assert reachable == {3, 4, 5, 7}


def test_rpq_grouped_reachable(graph, regex):
    reachable = rpq_bfs(
        graph, [0, 6], [0, 1, 2, 3, 4, 5, 7], regex, group_by_start=True
    )

    assert reachable == {0: {3, 4, 5, 7}, 6: {3, 4, 5, 7}}
