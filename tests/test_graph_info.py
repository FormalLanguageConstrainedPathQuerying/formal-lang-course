import cfpq_data

from project.graph_utils import *


def test_ring_graph_info():
    ring = cfpq_data.labeled_cycle_graph(
        n=3,
        label="x",
    )
    ring_info = graph_info_of(ring)
    assert ring_info == GraphInfo(
        number_of_nodes=3,
        number_of_edges=3,
        edge_labels={"x"},
    )


def test_two_connected_rings_info():
    two_connected_rings = cfpq_data.labeled_two_cycles_graph(
        n=2, m=3, labels=("x", "y")
    )
    two_connected_rings_info = graph_info_of(two_connected_rings)
    assert two_connected_rings_info == GraphInfo(
        number_of_nodes=6, number_of_edges=7, edge_labels={"x", "y"}
    )
