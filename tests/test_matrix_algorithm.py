import pytest
import project  # on import will print something from __init__ file
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from project.graph_utils import GraphUtils
from project.querying import query_to_graph_with_matrix_algorithm


def setup_module(module):
    print("helling setup module")


def teardown_module(module):
    print("helling teardown module")


def _check_querying(text: str, graph: MultiDiGraph, expected: set):
    actual = query_to_graph_with_matrix_algorithm(graph, CFG.from_text(text))
    assert actual == expected


def test_1_empty_matrix_algorithm():
    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))
    _check_querying(
        "\n".join(["S -> B A B ", "A -> a A a | a", "B -> b"]), graph, set()
    )
    print("test_1_empty_matrix_algorithm test asserted")


def test_2_simple_matrix_algorithm():
    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))

    _check_querying(
        "\n".join(["S -> A | B a", "A -> a", "B -> b"]), graph, {(0, 1), (1, 0), (3, 1)}
    )

    _check_querying(
        "\n".join(["S -> A B", "A -> a", "B -> b"]),
        graph,
        {(1, 2)},
    )

    _check_querying(
        "\n".join(["S -> A B", "A -> a | $", "B -> b"]),
        graph,
        {(2, 3), (0, 2), (1, 2), (3, 0)},
    )

    _check_querying(
        "\n".join(["S -> A | B", "A -> a", "B -> b"]),
        graph,
        {(0, 1), (3, 0), (2, 3), (0, 2), (1, 0)},
    )

    print("test_2_simple_matrix_algorithm test asserted")


def test_3_big_query_matrix_algorithm():
    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))
    _check_querying(
        "\n".join(["S -> B A B ", "A -> a A | a ", "B -> b | b b B b "]),
        graph,
        {(3, 2)},
    )

    _check_querying(
        "\n".join(["S -> B A B ", "A -> a A | a ", "B -> b | b b B "]),
        graph,
        {(0, 0), (0, 3), (2, 0), (3, 0), (2, 3), (0, 2), (3, 3), (2, 2), (3, 2)},
    )

    graph = GraphUtils.create_two_cycle_labeled_graph(2, 2, ("a", "b"))
    _check_querying(
        "\n".join(["S -> B A B ", "A -> a A a | a ", "B -> b | b b B "]),
        graph,
        {(4, 4), (4, 0), (0, 4), (3, 4), (4, 3), (0, 0), (0, 3), (3, 0), (3, 3)},
    )

    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))
    _check_querying(
        "\n".join(["S -> B A ", "A -> a A | a ", "B -> b | b b B A"]),
        graph,
        {(0, 1), (2, 1), (0, 0), (3, 1), (2, 0), (3, 0)},
    )
    print("test_3_big_query_matrix_algorithm test asserted")


def test_4_constrained_empty_matrix_algorithm():
    text = "\n".join(["F -> B A", "A -> a A | a ", "B -> b b B A | a "])
    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))
    actual = query_to_graph_with_matrix_algorithm(
        graph=graph,
        cfg=CFG.from_text(text, start_symbol="F"),
        start_var="F",
        start_nodes={0, 1},
        final_nodes={3},
    )
    assert actual == set()
    print("test_4_constrained_empty_matrix_algorithm test asserted")


def test_5_constrained_matrix_algorithm():
    text = "\n".join(["F -> B A", "A -> a A | b ", "B -> b B | a"])
    graph = GraphUtils.create_two_cycle_labeled_graph(1, 2, ("a", "b"))
    actual = query_to_graph_with_matrix_algorithm(
        graph=graph, cfg=text, start_var="F", start_nodes={3}, final_nodes={2}
    )
    assert actual == {(3, 2)}
    print("test_4_constrained_matrix_algorithm test asserted")
