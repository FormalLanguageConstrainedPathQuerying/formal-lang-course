from networkx import MultiDiGraph
from project.rpq_tensors import regular_path_query


def test_regular_path_query():
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
    regex = "(K|k)a.b(a+$)n*"

    reachable_pairs = regular_path_query(graph, [0, 6], [0, 1, 2, 3, 4, 5, 7], regex)

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
