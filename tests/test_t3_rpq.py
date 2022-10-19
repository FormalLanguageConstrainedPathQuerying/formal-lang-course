import cfpq_data
from scipy.sparse import lil_matrix

from project.t3_rpq import *


def test_rpq():
    graph = cfpq_data.labeled_two_cycles_graph(4, 7, labels=("a", "b"))
    regex = Regex("aa|aaa|(bb)*")
    result = rpq(graph, regex, {0}, {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, lil_matrix)
    assert result == {(0, 0), (0, 2), (0, 3), (0, 6), (0, 8), (0, 10)}
