from pathlib import Path

import networkx
from pyformlang.regular_expression import Regex

from project.automata.builders import build_nfa
from project.automata.rpq import rpq


class TestsForRpq:
    def test_rpq(self):
        graph = networkx.nx_pydot.read_dot(Path("./resources/dfa4.dot"))
        # dfa that accepts regex "a.b|a.c|(c.d)*"
        regex = Regex("a.b|a.c")

        expected = {("2", "1")}

        assert expected == rpq(
            regex, graph, start_nodes={"2"}, final_nodes={"0", "1", "2"}
        )
