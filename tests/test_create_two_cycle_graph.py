from project.graph import create_two_cycle_graph
import pytest
import networkx
import cfpq_data
import pydot
import os

def test_create_two_cycle_graph():
    nodes_left = 5
    nodes_right = 7
    first_label = "a"
    second_label = "b"
    name = "graph.dot"

    create_two_cycle_graph(
        nodes_left, nodes_right, (first_label, second_label), name
    )

    pydot_graph = pydot.graph_from_dot_file(name)[0]
    graph = networkx.nx_pydot.from_pydot(pydot_graph)

    assert graph.number_of_nodes() == nodes_right + nodes_left + 1
    assert graph.number_of_edges() == nodes_right + nodes_left + 2
    if (nodes_left < nodes_right):
        labels = [second_label, first_label]
    else:
        labels = [first_label, second_label]
    assert labels == cfpq_data.get_sorted_labels(graph)
    os.remove(name)
