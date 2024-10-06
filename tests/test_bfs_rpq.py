from project.bfs_rpq import ms_bfs_based_rpq

import networkx as nx


def test_ms_bfs_based_rpq():
    graph_from_lecture = nx.MultiDiGraph()
    graph_from_lecture.add_edge(0, 1, label="a")
    graph_from_lecture.add_edge(1, 2, label="a")
    graph_from_lecture.add_edge(0, 1, label="a")

    assert ms_bfs_based_rpq(
        "a",
        graph_from_lecture,
        {0},
        {1, 2},
    ) == {(0, 1)}
