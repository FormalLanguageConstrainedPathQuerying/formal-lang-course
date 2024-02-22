# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import pyformlang.finite_automaton
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


class GraphWordsHelper:
    graph = None
    all_paths = None

    def __init__(self, graph: MultiDiGraph):
        self.graph = graph
        self.all_paths = nx.shortest_path(graph)

    def is_reachable(self, source, target):
        if source not in self.all_paths.keys():
            return False
        return target in self.all_paths[source].keys()

    def _take_a_step(self, node):
        for node_to, edge_dict in dict(self.graph[node]).items():
            for edge_data in edge_dict.values():
                yield {"node_to": node_to, "label": edge_data["label"]}

    def _is_final_node(self, node):
        return self.graph.nodes(data=True)[node]["is_final"]

    def generate_words_by_node(self, node, word=None):
        if word is None:
            word = list()
        for trans in self._take_a_step(node):
            tmp = word.copy()
            label = trans["label"]
            if label != "ɛ":
                tmp.append(label)
            if self._is_final_node(trans["node_to"]):
                yield tmp.copy()
            yield from self.generate_words_by_node(trans["node_to"], tmp.copy())

    def take_words_by_node(self, node, n):
        final_nodes = list(map(lambda x: x[0], self.graph.nodes(data="is_final")))
        if any(
            map(lambda final_node: self.is_reachable(node, final_node), final_nodes)
        ):
            return itertools.islice(self.generate_words_by_node(node), 0, n)
        return []

    def get_all_words_less_then_n(self, n: int) -> list[str]:
        start_nodes = list(map(lambda x: x[0], self.graph.nodes(data="is_start")))
        result = list()
        for start in start_nodes:
            result.extend(self.take_words_by_node(start, n))
        return result


@pytest.fixture(scope="class", params=range(5))
def graph(request) -> MultiDiGraph:
    n_of_nodes = random.randint(1, 20)
    graph = nx.scale_free_graph(n_of_nodes)

    for _, _, data in graph.edges(data=True):
        data["label"] = random.choice(LABELS)

    return graph


class TestGraphToNfa:
    def test_not_specified(self, graph: MultiDiGraph) -> None:
        nfa: pyformlang.finite_automaton.NondeterministicFiniteAutomaton = graph_to_nfa(
            graph, set(), set()
        )
        words_helper = GraphWordsHelper(graph)
        words = words_helper.get_all_words_less_then_n(random.randint(10, 100))
        if len(words) == 0:
            assert nfa.is_empty()
        else:
            word = random.choice(words)
            assert nfa.accepts(word)

    def test_random(
        self,
        graph: MultiDiGraph,
    ) -> None:
        start_nodes = set(
            random.choices(
                list(graph.nodes().keys()), k=random.randint(1, len(graph.nodes))
            )
        )
        final_nodes = set(
            random.choices(
                list(graph.nodes().keys()), k=random.randint(1, len(graph.nodes))
            )
        )
        nfa: pyformlang.finite_automaton.NondeterministicFiniteAutomaton = graph_to_nfa(
            graph, start_nodes, final_nodes
        )
        words_helper = GraphWordsHelper(graph)
        words = words_helper.get_all_words_less_then_n(random.randint(10, 100))
        if len(words) == 0:
            assert nfa.is_empty()
        else:
            word = random.choice(words)
            assert nfa.accepts(word)
