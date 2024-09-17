import pytest
import cfpq_data
import networkx as nx

from project.graph import graph_init, graph_execute, Graph

available_names = cfpq_data.DATASET


@pytest.mark.parametrize("graph_name", available_names[:3])
def test_graph_init(graph_name):
    graph_current = graph_init(graph_name)

    graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_name))

    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()
    labels = set(cfpq_data.get_sorted_labels(graph))

    graph_expected = Graph(
        nodes,
        edges,
        labels,
    )

    assert graph_current == graph_expected


@pytest.mark.parametrize(
    [
        "first_cycle_nodes",
        "second_cycle_nodes",
        "labels",
        "graph_expected_path",
    ],
    [
        (
            3,
            2,
            ("test_message_one", "test_message_two"),
            "tests/graphs/first_graph.dot",
        ),
        (
            4,
            4,
            ("test_message_one", "test_message_two"),
            "tests/graphs/second_graph.dot",
        ),
    ],
)
def graph_execute_test(
    labels,
    path_temp,
    first_cycle_nodes,
    second_cycle_nodes,
    graph_expected_path,
):
    path_to_current = path_temp / "graph_temp.dot"
    graph_execute(first_cycle_nodes, second_cycle_nodes, labels, str(path_to_current))

    graph_current = nx.nx_pydot.read_dot(path_to_current)
    graph_expected = nx.nx_pydot.read_dot(graph_expected_path)

    assert nx.utils.graphs_equal(graph_expected, graph_current)
