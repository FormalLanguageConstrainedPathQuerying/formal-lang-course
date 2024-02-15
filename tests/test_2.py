import project.task2
from project.task2 import DeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import Symbol, Epsilon
import pytest
import pytest
import cfpq_data
import networkx
from project.task1 import build_and_save_graph_with_two_cicles, graph_info
import random
import pydot
import os



def generate_random_regex(length):
    symbols = ['a', 'b', "c", "d", "$"]

    rules = [
        lambda: f"({generate_random_regex(length = length-1)})",
        lambda: f"(({generate_random_regex(length = length-1)})|({generate_random_regex(length = length-1)}))",
        lambda: f"(({generate_random_regex(length = length-1)})*)",
        lambda: f"(({generate_random_regex(length = length-1)}).({generate_random_regex(length = length-1)}))"
    ]

    if length <= 1:
        regex = random.choice(symbols)
    else:
        regex = ''.join(random.choice(rules)() for _ in range(length))
    return regex


@pytest.mark.parametrize("length", list(range(6)))
def test_regex_to_dfa(length):
    random_regex = generate_random_regex(length)
    dfa = project.task2.regex_to_dfa(random_regex)
    assert (Regex(random_regex).accepts(random_regex) == dfa.accepts(random_regex))


test_graph_to_nfa_two_cicles_test_cases = [
    ["a", True],
    ["b", True],
    ["c", False],
    ["d", False],
    ["ab", True],
    ["ba", True],
    ["abc", False],
    ["abcd", False],
    ["abaa", False],
    ["baa", True]
]

@pytest.mark.parametrize("word, expected", test_graph_to_nfa_two_cicles_test_cases)
def test_graph_to_nfa_two_cicles(word, expected):
    n1 = random.randint(2, 4)
    n2 = random.randint(2, 4)
    file_path = os.path.abspath(f"test_resources/test_build_and_save_graph_with_two_cicles_{1}.dot")
    project.task1.build_and_save_graph_with_two_cicles(n1, n2, file_path)

    readed_graphs = pydot.graph_from_dot_file(file_path)
    readed_graph = networkx.drawing.nx_pydot.from_pydot(readed_graphs[0])

    nfa = project.task2.graph_to_nfa(readed_graph)


    assert nfa.accepts(word) == expected

    os.remove(file_path)

