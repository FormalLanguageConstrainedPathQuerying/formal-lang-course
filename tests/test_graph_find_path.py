from cProfile import label
from project import graph_find_path
import networkx as nx
from test_graphs import all_test_graphs


def generate_graph_by_word(word: str) -> nx.MultiDiGraph:
    res = nx.MultiDiGraph()
    counter = 0
    for c in word:
        res.add_edge(counter, counter + 1, label=c)
        counter += 1
    return res


def test_word_graph():
    for test in all_test_graphs:

        def fail_with(error: str) -> str:
            return f"{test.name} failed, {error}"

        for accept in test.accepts:
            res = graph_find_path(
                generate_graph_by_word(accept), test.reg, {0}, {len(accept)}
            )
            assert len(res) == 1, fail_with("graph_find_path found more than one path")
            start, finish = res.pop()
            assert start == 0, fail_with("graph_find_path start not 0")
            assert finish == len(accept), fail_with(
                f"graph_find_path finish not {len(accept)}"
            )
