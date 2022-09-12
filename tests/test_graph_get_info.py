from project.graph_utils import *


def test_two_cycle_graph_info():
    two_cycle_graph = cfpq_data.labeled_two_cycles_graph(n=3, m=3, labels=("A", "B"))
    two_cycle_graph_info = get_graph_info(two_cycle_graph)
    assert two_cycle_graph_info == GraphInfo(
        number_of_nodes=7,
        number_of_edges=8,
        edge_labels={"A", "B"},
    )


def test_wc_from_dataset():
    graph_info = get_graph_info_by_name("wc")
    assert graph_info == GraphInfo(
        number_of_edges=269,
        number_of_nodes=332,
        edge_labels={"A", "D"},
    )


test_wc_from_dataset()
