from project.task1 import get_graph_info
import pytest


def test_get_graph_info():
    info = get_graph_info("bzip")
    assert (632, 556, ['d', 'a']) == info
