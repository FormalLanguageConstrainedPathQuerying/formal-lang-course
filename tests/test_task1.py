import pytest
from project.task1.main import get_graph_info, save_two_cycles_graph
import os

def test_graph_info_no_file():
    with pytest.raises(FileNotFoundError):
        get_graph_info("homka")

def test_graph_info():
    graph_info = get_graph_info("bzip")
    assert graph_info.nodes_count == 632
    assert graph_info.edges_count == 556
    assert graph_info.edge_labels == ['a', 'd']

def test_save_two_cycles_graph():
    save_two_cycles_graph(10, 20, "tests/test_output.dot", ("A", "B"))
    with open("tests/test_task1.dot", "r") as test_file:
        with open("tests/test_output.dot") as test_output:
            assert test_file.read() == test_output.read()
    os.remove("tests/test_output.dot")