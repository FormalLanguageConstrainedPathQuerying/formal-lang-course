from pathlib import Path

import networkx
from pyformlang.regular_expression import Regex

from project.automata.rpq import rpq, bfs_rpq


class TestsForRpq:
    def test_rpq(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa4.dot"))
        # dfa that accepts regex "a.b|a.c|(c.d)*"
        regex = Regex("a.b|a.c")

        expected = {("2", "1")}

        assert expected == rpq(
            regex, graph, start_nodes={"2"}, final_nodes={"0", "1", "2"}
        )

    def test_bfs_rpq(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa4.dot"))
        # dfa that accepts regex "a.b|a.c|(c.d)*"
        regex = Regex("a.b|c.d|c.d.c.d|c.d.c.d.c.d")

        assert {"0", "1"} == bfs_rpq(
            regex,
            graph,
            start_nodes={"0", "2"},
            final_nodes={"0", "1", "2", "3", "4"},
            separate_flag=False,
        )
        assert {("2", "0"), ("2", "1"), ("0", "0")} == bfs_rpq(
            regex,
            graph,
            start_nodes={"0", "2"},
            final_nodes={"0", "1", "2", "3", "4"},
            separate_flag=True,
        )
