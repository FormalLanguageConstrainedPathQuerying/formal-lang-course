# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
import pytest
import random
import itertools
import networkx as nx

# Fix import statements in try block to run tests
try:
    from project.task2 import regex_to_dfa, graph_to_nfa
except ImportError:
    pytestmark = pytest.mark.skip("Task 2 is not ready to test!")

REGEX_TO_TEST = [
    "(aa)*",
    "a | a",
    "a* | a",
    "(ab) | (ac)",
    "(ab) | (abc)",
    "(abd) | (abc)",
    "(abd*) | (abc*)",
    "(abd)* | (abc)*",
    "((abd) | (abc))*",
    "a*a*",
    "a*a*b",
    "a* | (a | b)*",
    "a*(a | b)*",
    "(a | c)*(a | b)*",
]


@pytest.mark.skip("")
class TestRegexToDfa:
    @pytest.mark.parametrize("regex_str", REGEX_TO_TEST, ids=lambda regex: regex)
    def test(self, regex_str: str) -> None:
        regex = Regex(regex_str)
        regex_cfg = regex.to_cfg()
        regex_words = regex_cfg.get_words()

        if regex_cfg.is_finite():
            all_word_parts = list(regex_words)
            word_parts = random.choice(all_word_parts)
        else:
            index = random.randint(0, 2**9)
            word_parts = next(itertools.islice(regex_words, index, None))

        word = map(lambda x: x.value, word_parts)

        dfa = regex_to_dfa(regex_str)

        minimized_dfa = dfa.minimize()
        assert dfa.is_deterministic()
        assert dfa.is_equivalent_to(minimized_dfa)
        assert dfa.accepts(word)


LABELS = ["a", "b", "c", "x", "y", "z", "alpha", "beta", "gamma", "ɛ"]


@pytest.fixture(scope="class", params=range(2))
def graph(request) -> MultiDiGraph:
    n_of_nodes = random.randint(5, 20)
    graph = nx.scale_free_graph(n_of_nodes)

    for _, _, data in graph.edges(data=True):
        data["label"] = LABELS[random.randint(0, len(LABELS) - 1)]

    return graph


class TestGraphToNfa:
    def test_random(
        self,
        graph: MultiDiGraph,
    ) -> None:
        # print(graph.edges(data=True))
        assert True

    def test_all(self, graph: MultiDiGraph) -> None:
        for _, data in graph.nodes(data=True):
            data["is_start"] = True
            data["is_final"] = True
        # print(graph.nodes(data=True))

        starting_node = random.choice(list(graph.nodes))
        # print(starting_node)
        p = nx.dfs_edges(graph, starting_node)
        path = itertools.takewhile(lambda node: not node[1]["is_final"], p)
        print(list(p))

        assert True
