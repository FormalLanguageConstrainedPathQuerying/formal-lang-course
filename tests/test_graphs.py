from cProfile import label
from collections import namedtuple
import networkx as nx

from project.dfa_utils import graph_to_nfa

test_graph = namedtuple("test_graph", "name reg graph start_states final_states")


def binary_mess_ended_by_zero() -> test_graph:
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 0, label="1")
    graph.add_edge(0, 1, label="0")
    graph.add_edge(1, 1, label="0")
    graph.add_edge(1, 0, label="1")
    return test_graph("binary_mess_ended_by_zero", "(0|1)* 0", graph, {0}, {1})


def power_two() -> test_graph:
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="1")
    graph.add_edge(1, 1, label="0")
    return test_graph("power_two", "1 (0)*", graph, {0}, {1})


def banana_ananas() -> test_graph:
    reg_str = "("
    for i in range(ord("a"), ord("z") + 1):
        reg_str += "|" + chr(i)
    reg_str += "|_)* ((b a n a n a)|(a n a n a s))"

    graph = nx.MultiDiGraph()
    for i in range(ord("a"), ord("z") + 1):
        graph.add_edge(0, 0, label=chr(i))
    graph.add_edge(0, 0, label="_")
    graph.add_edge(0, 1, label="b")
    graph.add_edge(0, 2, label="a")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 3, label="n")
    graph.add_edge(3, 4, label="a")
    graph.add_edge(4, 5, label="n")
    graph.add_edge(5, 6, label="a")
    graph.add_edge(6, 7, label="s")

    return test_graph("banana_ananas", reg_str, graph, {0}, {6, 7})


all_test_graphs = [power_two(), binary_mess_ended_by_zero(), banana_ananas()]
