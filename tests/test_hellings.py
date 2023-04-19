from pyformlang.cfg import CFG, Variable
from project.graph_utils import create_two_cycles_graph
from project.hellings import hellings, hellings_context_free_path_query


def test_hellings():
    graph = create_two_cycles_graph((5, 5), ("a", "b"), "/tmp/graph")

    grammar = CFG.from_text("S -> a S b S | epsilon")

    assert hellings(graph, grammar) == {
        (0, Variable("S"), 0),
        (1, Variable("S"), 1),
        (2, Variable("S"), 2),
        (3, Variable("S"), 3),
        (4, Variable("S"), 4),
        (5, Variable("S"), 5),
        (6, Variable("S"), 6),
        (7, Variable("S"), 7),
        (8, Variable("S"), 8),
        (9, Variable("S"), 9),
        (10, Variable("S"), 10),
        (1, Variable("S"), 10),
        (2, Variable("S"), 9),
        (3, Variable("S"), 8),
        (4, Variable("S"), 7),
        (5, Variable("S"), 6),
        (0, Variable("a#CNF#"), 1),
        (1, Variable("a#CNF#"), 2),
        (2, Variable("a#CNF#"), 3),
        (3, Variable("a#CNF#"), 4),
        (4, Variable("a#CNF#"), 5),
        (5, Variable("a#CNF#"), 0),
        (10, Variable("b#CNF#"), 0),
        (0, Variable("b#CNF#"), 6),
        (6, Variable("b#CNF#"), 7),
        (7, Variable("b#CNF#"), 8),
        (8, Variable("b#CNF#"), 9),
        (9, Variable("b#CNF#"), 10),
        (10, Variable("C#CNF#1"), 0),
        (1, Variable("C#CNF#1"), 0),
        (6, Variable("C#CNF#1"), 7),
        (7, Variable("C#CNF#1"), 8),
        (8, Variable("C#CNF#1"), 9),
        (9, Variable("C#CNF#1"), 10),
        (5, Variable("C#CNF#1"), 7),
        (4, Variable("C#CNF#1"), 8),
        (0, Variable("C#CNF#1"), 6),
        (3, Variable("C#CNF#1"), 9),
        (2, Variable("C#CNF#1"), 10),
        (10, Variable("C#CNF#2"), 0),
        (0, Variable("C#CNF#2"), 6),
        (6, Variable("C#CNF#2"), 7),
        (7, Variable("C#CNF#2"), 8),
        (8, Variable("C#CNF#2"), 9),
        (9, Variable("C#CNF#2"), 10),
    }


def test_cfpq_hellings():
    graph = create_two_cycles_graph((5, 5), ("a", "b"), "/tmp/graph")
    grammar = CFG.from_text("S -> a S b S | epsilon")

    assert hellings_context_free_path_query(graph, grammar) == {
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (1, 10),
        (2, 9),
        (3, 8),
        (4, 7),
        (5, 6),
    }
