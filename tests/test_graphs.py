from cProfile import label
from collections import namedtuple
from os import access
import networkx as nx

test_graph = namedtuple(
    "test_graph", "name reg graph start_states final_states accepts rejects"
)


def empty_graph() -> test_graph:
    graph = nx.MultiDiGraph()
    accepts = []
    rejects = []
    return test_graph("empty_graph", "", graph, None, None, accepts, rejects)


def binary_mess_ended_by_zero() -> test_graph:
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 0, label="1")
    graph.add_edge(0, 1, label="0")
    graph.add_edge(1, 1, label="0")
    graph.add_edge(1, 0, label="1")

    accepts = []
    rejects = []
    for i in range(0, 42, 2):
        accepts.append("{0:b}".format(i))
        rejects.append("{0:b}".format(i + 1))

    return test_graph(
        "binary_mess_ended_by_zero", "(0|1)* 0", graph, {0}, {1}, accepts, rejects
    )


def power_two() -> test_graph:
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="1")
    graph.add_edge(1, 1, label="0")

    accepts = []
    rejects = []
    for i in range(2, 24, 2):
        accepts.append("{0:b}".format(2**i))
        rejects.append("{0:b}".format(i + 1))

    return test_graph("power_two", "1 (0)*", graph, {0}, {1}, accepts, rejects)


def zero_one() -> test_graph:
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="0")
    graph.add_edge(1, 0, label="1")

    accepts = set()
    accepts.add("0")
    rejects = []

    for i in range(1, 12):
        j = 0
        for g in range(1, i * 2 + 1, 2):
            j += 2**g
        accepts.add("{0:b}".format(j))
        accepts.add("{0:b}".format(j >> 1))
        accepts.add("0" + "{0:b}".format(j))
        accepts.add("0" + "{0:b}".format(j >> 1))

    counter = 0
    ind = 0
    while counter < 64:
        i = "{0:b}".format(ind)
        if not i in accepts:
            rejects.append(i)
            counter += 1
        ind += 1
    while counter < 128:
        i = "{0:b}".format(ind)
        if not i in accepts:
            rejects.append(i)
            counter += 1
        ind += 3

    accepts = list(accepts)

    return test_graph(
        "zero_one",
        "((0|(1 0)) (((1 0)*)|((1 0)* 1)))|1",
        graph,
        {0, 1},
        {0, 1},
        accepts,
        rejects,
    )


def banana_ananas() -> test_graph:
    reg_str = "("
    for i in range(ord("a"), ord("z") + 1):
        reg_str += chr(i) + "|"
    reg_str += "_)* ((b a n a n a)|(a n a n a s))"

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

    accepts = ["banana", "ananas", "mama_love_bananas"]
    rejects = ["banana_not_apple", "banana_is_bad", "ananas_is_not_pineapple"]

    return test_graph("banana_ananas", reg_str, graph, {0}, {6, 7}, accepts, rejects)


def labels_as_nodes():
    reg_str = "n a*"
    graph = nx.MultiDiGraph()
    graph.add_edge("a", "b", label="n")
    graph.add_edge("b", "b", label="a")

    accepts = ["n", "na", "naa", "naaa", "naaaa"]
    rejects = ["a", "an", "banana", "ananas", "nanana"]

    return test_graph("labels_as_nodes", reg_str, graph, {"a"}, {"b"}, accepts, rejects)


all_test_graphs = [
    empty_graph(),
    power_two(),
    binary_mess_ended_by_zero(),
    zero_one(),
    banana_ananas(),
    labels_as_nodes(),
]


def accepting_test(acceptable, graph: test_graph):
    for accept in graph.accepts:
        assert acceptable.accepts(
            accept
        ), f'{graph.name} failed, "{accept}" not accepted'
    for reject in graph.rejects:
        assert not acceptable.accepts(
            reject
        ), f'{graph.name} failed, "{reject}" not rejected'
