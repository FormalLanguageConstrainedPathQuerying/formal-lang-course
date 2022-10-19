from project import rpq_reg_str
import networkx as nx
from test_graphs import all_test_graphs, banana_ananas, empty_graph


def generate_graph_by_word(word: str) -> nx.MultiDiGraph:
    res = nx.MultiDiGraph()
    counter = 0
    for c in word:
        res.add_edge(counter, counter + 1, label=c)
        counter += 1
    return res


def test_rpq_word_graph():
    for test in all_test_graphs:

        def fail_with(error: str) -> str:
            return f"{test.name} failed, {error}"

        for accept in test.accepts:
            res = rpq_reg_str(
                generate_graph_by_word(accept), test.reg, {0}, {len(accept)}
            )
            assert len(res) == 1, fail_with("rpq_by_reg_str found more than one path")
            start, finish = res.pop()
            assert start == 0, fail_with("rpq_by_reg_str start not 0")
            assert finish == len(accept), fail_with(
                f"rpq_by_reg_str finish not {len(accept)}"
            )


def test_rpq_banana_ananas():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="b")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 1, label="n")
    graph.add_edge(2, 3, label="s")
    res = rpq_reg_str(graph, banana_ananas().reg)
    assert res == {(0, 2), (0, 3), (1, 3), (2, 3)}


def test_rpq_empty_some():
    empty = empty_graph()
    for some in all_test_graphs:
        for a, b in ((some, empty), (empty, some)):
            assert (
                len(rpq_reg_str(a.graph, b.reg, a.start_states, a.final_states)) == 0
            ), f"rpq_by_reg_str({a.name}, {b.name}) is not empty set"
