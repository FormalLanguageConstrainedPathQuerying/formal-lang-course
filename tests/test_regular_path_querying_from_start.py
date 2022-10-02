from project import regular_path_querying_from_start
import networkx as nx
from test_graphs import all_test_graphs, banana_ananas, empty_graph


def generate_graph_by_word(word: str) -> nx.MultiDiGraph:
    res = nx.MultiDiGraph()
    counter = 0
    for c in word:
        res.add_edge(counter, counter + 1, label=c)
        counter += 1
    return res


def test_regular_path_querying_from_start_banana_ananas():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="b")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 1, label="n")
    graph.add_edge(2, 3, label="s")
    res = regular_path_querying_from_start(graph, banana_ananas().reg, {0})
    assert res == {2, 3}


def test_regular_path_querying_from_separately_start_banana_ananas():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="b")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 1, label="n")
    graph.add_edge(2, 3, label="s")
    res = regular_path_querying_from_start(graph, banana_ananas().reg, {0}, True)
    assert res == {(0, 2), (0, 3)}
    res = regular_path_querying_from_start(graph, banana_ananas().reg, {0, 1, 3}, True)
    assert res == {(0, 2), (0, 3), (1, 3)}
    res = regular_path_querying_from_start(graph, banana_ananas().reg, {1, 2, 3}, True)
    assert res == {(1, 3), (2, 3)}
    res = regular_path_querying_from_start(
        graph, banana_ananas().reg, {0, 1, 2, 3}, True
    )
    assert res == {(0, 2), (0, 3), (1, 3), (2, 3)}


def test_regular_path_querying_from_start_empty_some():
    empty = empty_graph()
    for some in all_test_graphs:
        for a, b in ((some, empty), (empty, some)):
            assert (
                len(regular_path_querying_from_start(a.graph, b.reg, a.start_states))
                == 0
            ), f"graph_find_path({a.name}, {b.name}) is not empty set"
