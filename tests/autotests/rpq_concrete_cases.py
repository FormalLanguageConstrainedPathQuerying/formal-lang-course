from typing import Callable

import graphs
from copy import copy
from networkx import MultiDiGraph


class CaseRPQ:
    """
    class that contains all information about test case for rpq algorithms
    """

    def __init__(
        self,
        graph: MultiDiGraph,
        regex: str,
        actual_answer: set[tuple[int, int]],
        start_nodes: set[int] = None,
        final_nodes: set[int] = None,
    ):
        self.graph = copy(graph)
        self.regex = copy(regex)
        self.expected_answer = copy(actual_answer)
        self.start_nodes = copy(start_nodes) if start_nodes else graph.nodes
        self.final_nodes = copy(final_nodes) if final_nodes else graph.nodes

    def check_answer_regex(
        self,
        function: Callable[
            [str, MultiDiGraph, set[int], set[int]], set[tuple[int, int]]
        ],
    ):
        """
        assertion function for algorithms with regex
        :param function: the function under test (*tensor_based_rpq*)
        :return: assertion
        """
        assert (
            function(self.regex, self.graph, self.start_nodes, self.final_nodes)
            == self.expected_answer
        )


CASES_RPQ = [
    CaseRPQ(graphs.point_graph, "a", set()),
    CaseRPQ(graphs.point_graph, "a*", {(1, 1)}),
    CaseRPQ(graphs.set_of_vertices_without_edges, "a*", {(0, 0), (2, 2), (1, 1)}),
    CaseRPQ(graphs.b_graph, "a", set()),
    CaseRPQ(graphs.b_graph, "b", {(0, 1)}),
    CaseRPQ(graphs.b_graph, "b*", {(0, 1), (0, 0), (1, 1)}),
    CaseRPQ(
        graphs.bbb_graph,
        "(b b)*",
        {(0, 1), (0, 0), (0, 2), (1, 1), (1, 2), (1, 0), (2, 2), (2, 1), (2, 0)},
    ),
    CaseRPQ(
        graphs.bab_graph,
        "(a | b)*",
        {(0, 1), (0, 0), (0, 2), (1, 1), (1, 2), (1, 0), (2, 2), (2, 1), (2, 0)},
    ),
]
