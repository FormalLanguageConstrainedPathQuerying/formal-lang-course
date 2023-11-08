import pytest
from collections import namedtuple
from itertools import product
from cfpq_data import labeled_cycle_graph, labeled_two_cycles_graph
from pyformlang.cfg import CFG

from project.hellings_alg import hellings_alg, cfpq


Config = namedtuple(
    "Config", ["start_var", "start_nodes", "final_nodes", "expected_result"]
)


@pytest.mark.parametrize(
    "cfg, graph, expected_result",
    [
        (
            """
            S -> epsilon
            """,
            labeled_cycle_graph(3, "a"),
            {(1, "S", 1), (2, "S", 2), (0, "S", 0)},
        ),
        (
            """
                S -> b | epsilon
                """,
            labeled_cycle_graph(4, "b"),
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
            labeled_two_cycles_graph(2, 1, labels=("a", "b")),
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
def test_hellings_answer(cfg, graph, expected_result):
    assert hellings_alg(graph, CFG.from_text(cfg)) == expected_result


@pytest.mark.parametrize(
    "cfg, graph, confs",
    [
        (
            """
                A -> a A | epsilon
                B -> b B | b
                """,
            labeled_cycle_graph(3, "a"),
            [
                Config("A", {0}, {0}, {(0, 0)}),
                Config("A", None, None, set(product(range(3), range(3)))),
                Config("B", None, None, set()),
            ],
        ),
        (
            """
                S -> epsilon
                """,
            labeled_cycle_graph(4, "b"),
            [
                Config("S", {0, 1}, {0, 1}, {(0, 0), (1, 1)}),
                Config("S", None, None, set((v, v) for v in range(4))),
                Config("B", None, None, set()),
            ],
        ),
        (
            """
                    S -> A B
                    S -> A S1
                    S1 -> S B
                    A -> a
                    B -> b
                    """,
            labeled_two_cycles_graph(2, 1, labels=("a", "b")),
            [
                Config(
                    "S", None, None, {(0, 0), (0, 3), (2, 0), (2, 3), (1, 0), (1, 3)}
                ),
                Config("A", None, None, {(0, 1), (1, 2), (2, 0)}),
                Config("B", None, None, {(3, 0), (0, 3)}),
                Config("S", {0}, {0}, {(0, 0)}),
            ],
        ),
    ],
)
def test_cfpq_answer(cfg, graph, confs):
    assert all(
        cfpq(
            graph,
            CFG.from_text(cfg),
            conf.start_nodes,
            conf.final_nodes,
            conf.start_var,
        )
        == conf.expected_result
        for conf in confs
    )