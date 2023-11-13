from pathlib import Path

import networkx as nx
from pyformlang.cfg import Variable

from project.cfg.cfpq.hellings import cfpq_all, cfpq
from project.cfg.io import read_from_file


class TestForHellingCfpq:
    def test_cfpq_helling(self):
        cfg = read_from_file(Path("./resources/cfg2"), "S")

        graph = nx.MultiDiGraph()
        graph.add_edge(0, 1, label="a")
        graph.add_edge(1, 2, label="a")
        graph.add_edge(2, 0, label="a")
        graph.add_edge(2, 3, label="b")
        graph.add_edge(3, 2, label="b")

        # Test from lecture notes (page 113)
        assert cfpq_all(cfg, graph) == {
            (0, Variable("S"), 2),
            (2, Variable("C"), 3),
            (1, Variable("A"), 2),
            (1, Variable("S"), 2),
            (2, Variable("S"), 2),
            (0, Variable("S"), 3),
            (0, Variable("A"), 1),
            (0, Variable("C"), 2),
            (1, Variable("S"), 3),
            (2, Variable("S"), 3),
            (1, Variable("C"), 2),
            (3, Variable("B"), 2),
            (2, Variable("A"), 0),
            (2, Variable("C"), 2),
            (2, Variable("B"), 3),
            (0, Variable("C"), 3),
            (1, Variable("C"), 3),
        }

    def test_cfpq(self):
        cfg = read_from_file(Path("./resources/cfg1"), "S")

        graph = nx.MultiDiGraph()
        graph.add_edge(0, 1, label="a")
        graph.add_edge(1, 2, label="a")
        graph.add_edge(2, 3, label="b")
        graph.add_edge(3, 4, label="b")
        graph.add_edge(4, 5, label="a")
        graph.add_edge(5, 6, label="b")
        # graph with all substrings of string "aabbab"

        cfpq_result = cfpq(cfg, graph)

        # should have all correct bracket sequence substrings of "aabbab"
        not_empty_result = {elem for elem in cfpq_result if elem[0] != elem[1]}
        assert not_empty_result == {(0, 4), (4, 6), (0, 6), (1, 3)}
