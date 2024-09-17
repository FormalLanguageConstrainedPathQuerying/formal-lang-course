import networkx as nx
import cfpq_data
import pytest
from project.task1 import get_graph_data, save_labeled_two_cycles_graph, GraphData


@pytest.mark.parametrize(
    "name, expected_node_count, expected_edge_count, expected_labels",
    [("wc", 332, 269, {"a", "d"}), ("ls", 1687, 1453, {"a", "d"})],
)
def test_get_graph_data(
    name, expected_node_count, expected_edge_count, expected_labels
):
    graph = get_graph_data(name)

    assert isinstance(graph, GraphData)
    assert graph.node_count == expected_node_count
    assert graph.edge_count == expected_edge_count
    assert set(graph.labels) == expected_labels


EXPECTED_GRAPHS_FOLDER = "tests/test_graphs"


@pytest.mark.parametrize(
    "n, m, labels, dot_filename",
    [
        (3, 4, ["a", "b"], "graph_3_4_ab.dot"),
        (5, 5, ["x", "y"], "graph_5_5_xy.dot"),
        (2, 3, ["label1", "label2"], "graph_2_3_label1_label2.dot"),
    ],
)
def test_create_labeled_two_cycles_graph(tmp_path, n, m, labels, dot_filename):
    test_path = tmp_path / "test.dot"

    save_labeled_two_cycles_graph(n, m, labels, test_path)

    assert test_path.exists()

    generated_graph = nx.nx_pydot.read_dot(str(test_path))

    expected_graph_path = f"{EXPECTED_GRAPHS_FOLDER}/{dot_filename}"
    expected_graph = nx.nx_pydot.read_dot(expected_graph_path)

    assert isinstance(generated_graph, nx.MultiDiGraph)
    assert generated_graph.number_of_nodes() == n + m + 1
    assert set(cfpq_data.get_sorted_labels(generated_graph)) == set(labels)

    assert nx.is_isomorphic(generated_graph, expected_graph)
