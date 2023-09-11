from networkx import MultiDiGraph
from project.graph_lib import save_graph


def test_save_graph():
    path = "tests/generated/sgt_graph.dot"
    path_truth = "tests/test_graphs/sgt_graph_truth.dot"

    G = MultiDiGraph()
    G.add_nodes_from([0, 1])
    G.add_edges_from([(0, 1, {"label": "a"}), (1, 0, {"label": "b"})])

    save_graph(G, path)

    with open(path, "r") as f:
        with open(path_truth, "r") as t:
            assert f.readlines() == t.readlines()
