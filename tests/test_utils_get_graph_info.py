from project import *
import cfpq_data


def test_by_labeled_two_cycles_graph():
    g = cfpq_data.labeled_two_cycles_graph(42, 29, labels=("a", "b"))
    info = get_graph_info(g)
    assert info.number_of_nodes == 72
    assert info.number_of_edges == 73
    assert info.lables == {"a", "b"}
