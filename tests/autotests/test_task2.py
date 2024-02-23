# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import copy

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


LABELS = ["a", "b", "c", "x", "y", "z", "alpha", "beta", "gamma"]
LABEL = "label"
IS_FINAL = "is_final"
IS_START = "is_start"


class GraphWordsHelper:
    graph = None
    final_nodes = None
    transitive_closure = None
    start_nodes = None

    def __init__(self, graph: MultiDiGraph):
        self.graph = graph.copy()
        self.final_nodes = list(
            map(lambda x: x[0], filter(lambda y: y[1], self.graph.nodes(data=IS_FINAL)))
        )
        self.start_nodes = list(
            map(lambda x: x[0], filter(lambda y: y[1], self.graph.nodes(data=IS_START)))
        )
        self.transitive_closure: nx.MultiDiGraph = nx.transitive_closure(
            copy.deepcopy(self.graph), reflexive=False
        )

    def is_reachable(self, source, target):
        return target in self.transitive_closure[source].keys()

    def _exists_any_final_path(self, node):
        for final_node in self.final_nodes:
            if self.is_reachable(node, final_node):
                return True
        return False

    def _take_a_step(self, node):
        for node_to, edge_dict in dict(self.graph[node]).items():
            for edge_data in edge_dict.values():
                yield node_to, edge_data[LABEL]

    def _is_final_node(self, node):
        return node in self.final_nodes

    def generate_words_by_node(self, node):
        queue = [(node, [])]
        while len(queue) != 0:
            (n, word) = queue.pop(0)
            for node_to, label in self._take_a_step(n):
                tmp = word.copy()
                tmp.append(label)
                if self._is_final_node(node_to):
                    yield tmp.copy()
                if self._exists_any_final_path(node_to):
                    queue.append((node_to, tmp.copy()))

    def take_n_words_by_node(self, node, n):
        if self._exists_any_final_path(node):
            return list(itertools.islice(self.generate_words_by_node(node), 0, n))
        return []

    def get_words_with_limiter(self, limiter: int) -> list[str]:
        result = list()
        for start in self.start_nodes:
            result.extend(self.take_n_words_by_node(start, limiter))
            if start in self.final_nodes:
                result.append([])
        return result


@pytest.fixture(scope="class", params=range(8))
def graph(request) -> MultiDiGraph:
    n_of_nodes = random.randint(1, 20)
    graph = nx.scale_free_graph(n_of_nodes)

    for _, _, data in graph.edges(data=True):
        data[LABEL] = random.choice(LABELS)
    for _, data in graph.nodes(data=True):
        data[IS_FINAL] = False
        data[IS_START] = False
    return graph


class TestGraphToNfa:
    def test_random_start_and_final(
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
            graph.copy(), start_nodes.copy(), final_nodes.copy()
        )
        for node, data in graph.nodes(data=True):
            if node in start_nodes:
                data[IS_START] = True
            if node in final_nodes:
                data[IS_FINAL] = True
        words_helper = GraphWordsHelper(graph)
        words = words_helper.get_words_with_limiter(random.randint(10, 100))
        if len(words) == 0:
            assert nfa.is_empty()
        else:
            word = random.choice(words)
            assert nfa.accepts(word)

    def test_not_specified_start_and_final(self, graph: MultiDiGraph) -> None:
        nfa: pyformlang.finite_automaton.NondeterministicFiniteAutomaton = graph_to_nfa(
            graph.copy(), set(), set()
        )
        for _, data in graph.nodes(data=True):
            data[IS_FINAL] = True
            data[IS_START] = True
        words_helper = GraphWordsHelper(graph)
        words = words_helper.get_words_with_limiter(random.randint(10, 100))
        if len(words) == 0:
            assert nfa.is_empty()
        else:
            word = random.choice(words)
            assert nfa.accepts(word)
