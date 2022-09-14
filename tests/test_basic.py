import os

import pytest
from project.graphs_util import *


def test_works_as_expected_for_get_info_function():
    result = get_info_by_graph_name("generations")
    assert result[0] == 129
    assert result[1] == 273


def test_works_as_expected():
    create_and_save_graph(1, 1, "a", "b", "file_for_test.dot")
    assert (
        open("file_for_test.dot", "r").read()
        == """digraph  {
1;
0;
2;
1 -> 0  [key=0, label=a];
0 -> 1  [key=0, label=a];
0 -> 2  [key=0, label=b];
2 -> 0  [key=0, label=b];
}
"""
    )
    os.remove("file_for_test.dot")
