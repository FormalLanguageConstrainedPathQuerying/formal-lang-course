from project.task1 import create_two_cycle_graph
import filecmp
import networkx
import cfpq_data
import pydot
import os

def test_create_two_cycle_graph():
    nodes_left = 5
    nodes_right = 7
    first_label = "a"
    second_label = "b"
    name = "test_graph.dot"

    create_two_cycle_graph(
        nodes_left, nodes_right, (first_label, second_label), name
    )
    assert filecmp.cmp("tests/resources/two_cycle_graph.dot", "test_graph.dot", shallow=False)
    current_dir = os.getcwd()
    print("Current directory:", current_dir)
    with open("tests/resources/two_cycle_graph.dot", "r") as resource_graph:
        with open(f"{name}") as output_graph:
            assert resource_graph.read() == output_graph.read()

    pydot_graph = pydot.graph_from_dot_file("tests/resources/two_cycle_graph.dot")[0]
    resource_graph = networkx.nx_pydot.from_pydot(pydot_graph)

    pydot_graph = pydot.graph_from_dot_file(f"{name}")[0]
    output_graph = networkx.nx_pydot.from_pydot(pydot_graph)

    assert resource_graph.number_of_nodes() == output_graph.number_of_nodes()
    assert resource_graph.number_of_edges() == output_graph.number_of_edges()
    assert cfpq_data.get_sorted_labels(resource_graph) == cfpq_data.get_sorted_labels(output_graph)
    os.remove(name)
