import pytest
import cfpq_data
import networkx as nx

from project.graph_utils import (
    get_graph,
    create_labeled_two_cycles_graph,
    Graph,
    graph_to_nfa,
)

available_graphs_name = cfpq_data.DATASET


@pytest.mark.parametrize("graph_name", available_graphs_name[:3])
def test_get_graph(graph_name):
    actual_graph = get_graph(graph_name)

    graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_name))
    expected_graph = Graph(
        node_count=graph.number_of_nodes(),
        edge_count=graph.number_of_edges(),
        edge_labels=set(cfpq_data.get_sorted_labels(graph)),
    )

    assert actual_graph == expected_graph


@pytest.mark.parametrize(
    [
        "first_cycle_node_count",
        "second_cycle_node_count",
        "labels",
        "expected_graph_path",
    ],
    [
        (3, 2, ("a", "b"), "tests/test_data/utils/expected_graph_3_2.dot"),
        (4, 4, ("haha", "hihi"), "tests/test_data/utils/expected_graph_4_4.dot"),
    ],
)
def test_create_labeled_two_cycles_graph(
    tmp_path,
    labels,
    expected_graph_path,
    first_cycle_node_count,
    second_cycle_node_count,
):
    path_to_actual = tmp_path / "tmp_graph.dot"
    create_labeled_two_cycles_graph(
        first_cycle_node_count, second_cycle_node_count, labels, str(path_to_actual)
    )

    actual_graph = nx.nx_pydot.read_dot(path_to_actual)
    expected_graph = nx.nx_pydot.read_dot(expected_graph_path)

    assert nx.utils.graphs_equal(expected_graph, actual_graph)


def test_two_cycles_graph_to_nfa():
    first_cycle_node_count = 3
    second_cycle_node_count = 2
    first_label = "a"
    second_label = "b"
    graph = create_labeled_two_cycles_graph(
        first_cycle_node_count,
        second_cycle_node_count,
        labels=(first_label, second_label),
    )
    nfa = graph_to_nfa(graph, set(), set())

    start_states = set(int(st.value) for st in nfa.start_states)
    final_states = set(int(st.value) for st in nfa.final_states)

    assert (
        len(start_states)
        == len(final_states)
        == first_cycle_node_count + second_cycle_node_count + 1
    )
    assert nfa.symbols == {first_label, second_label}
