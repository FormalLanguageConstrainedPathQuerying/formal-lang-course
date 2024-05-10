# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
import pytest
import random
import itertools
from helper import GraphWordsHelper, generate_rnd_start_and_final
from constants import IS_FINAL, IS_START
from fixtures import graph
from grammars_constants import REGEXES

# Fix import statements in try block to run tests
try:
    from project.task2 import regex_to_dfa, graph_to_nfa
except ImportError:
    pytestmark = pytest.mark.skip("Task 2 is not ready to test!")


class TestRegexToDfa:
    @pytest.mark.parametrize("regex_str", REGEXES)
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


class TestGraphToNfa:
    def test_random_start_and_final(
        self,
        graph: MultiDiGraph,
    ) -> None:
        copy_graph = graph.copy()
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        nfa: NondeterministicFiniteAutomaton = graph_to_nfa(
            copy_graph, start_nodes.copy(), final_nodes.copy()
        )
        words_helper = GraphWordsHelper(graph)
        words = words_helper.get_words_with_limiter(random.randint(10, 100))
        if len(words) == 0:
            assert nfa.is_empty()
        else:
            word = random.choice(words)
            assert nfa.accepts(word)

    def test_not_specified_start_and_final(self, graph: MultiDiGraph) -> None:
        nfa: NondeterministicFiniteAutomaton = graph_to_nfa(graph.copy(), set(), set())
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
