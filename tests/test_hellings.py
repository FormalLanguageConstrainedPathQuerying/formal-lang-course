import pytest
from pyformlang.cfg import CFG

from project.grammars.hellings import hellings
from project.utils.graph_utils import generate_two_cycles_graph
from cfpq_data import labeled_cycle_graph


@pytest.mark.parametrize(
    "cfg, graph, exp_ans",
    [
        (
            """
            S -> epsilon
            """,
            labeled_cycle_graph(3, "a", verbose=False),
            {(1, "S", 1), (2, "S", 2), (0, "S", 0)},
        ),
        (
            """
                S -> b | epsilon
                """,
            labeled_cycle_graph(4, "b", verbose=False),
            {
                (1, "S", 1),
                (2, "S", 2),
                (0, "S", 0),
                (3, "S", 3),
                (0, "S", 1),
                (1, "S", 2),
                (2, "S", 3),
                (3, "S", 0),
            },
        ),
        (
            """
                S -> A B
                S -> A S1
                S1 -> S B
                A -> a
                B -> b
                """,
            generate_two_cycles_graph("2", "1", "a", "b"),
            {
                (0, "S1", 3),
                (2, "S1", 0),
                (2, "S", 3),
                (2, "S1", 3),
                (3, "B", 0),
                (1, "S", 0),
                (0, "S", 0),
                (1, "S", 3),
                (1, "A", 2),
                (0, "S", 3),
                (0, "B", 3),
                (1, "S1", 3),
                (2, "A", 0),
                (1, "S1", 0),
                (0, "S1", 0),
                (0, "A", 1),
                (2, "S", 0),
            },
        ),
    ],
)
def test_hellings_answer(cfg, graph, exp_ans):
    assert hellings(CFG.from_text(cfg), graph) == exp_ans
