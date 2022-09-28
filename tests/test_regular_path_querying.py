from project import regular_path_querying
import networkx as nx
from test_graphs import all_test_graphs, banana_ananas, empty_graph


def generate_graph_by_word(word: str) -> nx.MultiDiGraph:
    res = nx.MultiDiGraph()
    counter = 0
    for c in word:
        res.add_edge(counter, counter + 1, label=c)
        counter += 1
    return res


def test_graph_find_path_word_graph():
    for test in all_test_graphs:

        def fail_with(error: str) -> str:
            return f"{test.name} failed, {error}"

        for accept in test.accepts:
            res = regular_path_querying(
                generate_graph_by_word(accept), test.reg, {0}, {len(accept)}
            )
            assert len(res) == 1, fail_with("graph_find_path found more than one path")
            start, finish = res.pop()
            assert start == 0, fail_with("graph_find_path start not 0")
            assert finish == len(accept), fail_with(
                f"graph_find_path finish not {len(accept)}"
            )


def test_graph_find_path_banana_ananas():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="b")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 1, label="n")
    graph.add_edge(2, 3, label="s")
    res = regular_path_querying(graph, banana_ananas().reg)
    assert res == {(0, 2), (0, 3), (1, 3), (2, 3)}


def test_graph_find_path_empty_some():
    empty = empty_graph()
    for some in all_test_graphs:
        for a, b in ((some, empty), (empty, some)):
            assert (
                len(
                    regular_path_querying(
                        a.graph, b.reg, a.start_states, a.final_states
                    )
                )
                == 0
            ), f"graph_find_path({a.name}, {b.name}) is not empty set"
