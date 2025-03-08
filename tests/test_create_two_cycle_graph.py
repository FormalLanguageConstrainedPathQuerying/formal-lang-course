from project.task1 import create_two_cycle_graph
import filecmp
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

    with open("tests/resources/two_cycle_graph.dot", "r") as resource_graph:
        with open(f"{name}") as output_graph:
            assert resource_graph.read() == output_graph.read()

    os.remove(name)
