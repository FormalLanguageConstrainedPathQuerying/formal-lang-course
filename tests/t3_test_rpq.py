import cfpq_data

from project.t3_rpq import *


def test_rqp():
    graph = cfpq_data.labeled_two_cycles_graph(4, 7, labels=("a", "b"))
    regex = PythonRegex("aa|aaa|(bb)*")
    result = rpq(graph, regex, {0}, {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11})
    assert result == {(0, 0), (0, 2), (0, 3), (0, 6), (0, 8), (0, 10)}
