import pytest
import cfpq_data
from project import utils


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_getting_graph_info():
    graph = cfpq_data.labeled_two_cycles_graph(
        10, 5, edge_labels=("a", "b"), verbose=False
    )
    g_info = utils.get_graph_info(graph)
    assert g_info[0] == 16
    assert g_info[1] == 17
    assert g_info[2] == {"a", "b"}


def test_saving_graph():
    utils.generate_and_export_two_cycle(
        10, 5, ("a", "b"), "tests/data/example_saving.dot"
    )
