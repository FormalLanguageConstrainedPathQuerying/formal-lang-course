import pytest
from project import *
import cfpq_data


def test_by_labeled_two_cycles_graph():
    g = cfpq_data.labeled_two_cycles_graph(42, 29, labels=("a", "b"))
    assert get_graph_info(g) == graph_info(72, 73, {"a", "b"})
