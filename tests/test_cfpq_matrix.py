import pytest

from networkx import MultiDiGraph
from pyformlang.cfg import CFG

from project.graph_utils import *
from project.cfpq import *


@pytest.mark.parametrize(
    "cfg_as_text, graph, reachable_pairs",
    [
        (
            """
            """,
            MultiDiGraph(),
            set(),
        ),
        (
            """
            S ->
            S -> a S b S
            """,
            MultiDiGraph(),
            set(),
        ),
        (
            """
            S ->
            """,
            create_two_cycle_labeled_graph(1, 1, ("a", "b")),
            {(0, 0), (1, 1), (2, 2)},
        ),
        (
            """
            S -> a b
            S -> a S b
            """,
            create_two_cycle_labeled_graph(1, 1, ("a", "b")),
            {(1, 2), (0, 0)},
        ),
        (
            """
            S ->
            S -> a b
            S -> b a
            """,
            create_two_cycle_labeled_graph(1, 1, ("a", "b")),
            {(1, 2), (2, 1), (0, 0), (1, 1), (2, 2)},
        ),
        (
            """
            S -> a
            S -> a S
            """,
            create_two_cycle_labeled_graph(1, 1, ("a", "b")),
            {(0, 1), (1, 0), (1, 1), (0, 0)},
        ),
    ],
)
def test_cfpq(cfg_as_text, graph, reachable_pairs):
    assert (
        cfpq(
            algo=CFPQAlgorithm.MATRIX,
            graph=graph,
            cfg=CFG.from_text(cfg_as_text),
            start_nodes=None,
            final_nodes=None,
        )
        == reachable_pairs
    )
