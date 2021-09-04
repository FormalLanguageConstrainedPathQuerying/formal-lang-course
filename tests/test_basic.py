import cfpq_data

from project.graphs import get_graph_info, generate_and_save_two_cycles


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_getting_graph_info():
    graph = cfpq_data.labeled_binomial_graph(
        42, 1, seed=42, edge_labels=["one", "two", "three"], verbose=False
    )
    g_info = get_graph_info(graph)
    assert g_info.nodes_count == 42
    assert g_info.edges_count == 1722
    assert g_info.labels == {"one", "two", "three"}


def test_saving_graph():
    generate_and_save_two_cycles(10, 15, ("a", "b"), "../resources/example_saving.dot")
