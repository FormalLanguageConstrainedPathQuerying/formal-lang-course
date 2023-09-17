from typing import List, Tuple
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import Symbol, DeterministicFiniteAutomaton
from project.finite_automata_construct import regex_to_min_dfa


def construct_regex_and_dfa(regex: str) -> Tuple[Regex, DeterministicFiniteAutomaton]:
    return Regex(regex), regex_to_min_dfa(regex)


def strs_to_word(strs: List[str]) -> List[Symbol]:
    return [Symbol(s) for s in strs]


def test_concat_regex():
    regex, dfa = construct_regex_and_dfa("ab.bc.cd")

    for test_case in [
        ["abbccd"],
        ["ab", "bc", "cd"],
        ["a", "b", "b", "c", "c", "d"],
        ["a", "b"],
        ["a", "b"],
    ]:
        assert regex.accepts(test_case) == dfa.accepts(strs_to_word(test_case))


def test_union_regex():
    regex, dfa = construct_regex_and_dfa("abc|d+ef")

    for test_case in [
        ["abc"],
        ["abc", "d", "ef"],
        ["a", "b", "c", "d", "e", "f"],
        ["d"],
        ["ef"],
    ]:
        assert regex.accepts(test_case) == dfa.accepts(strs_to_word(test_case))


def test_star_regex():
    regex, dfa = construct_regex_and_dfa("a*bc*a")

    for test_case in [
        ["a"],
        ["a", "a"],
        ["bc", "a"],
        ["a", "bc", "a"],
        ["a", "a", "bc", "bc", "bc", "a"],
        ["a", "bc", "bc"],
        ["abc", "a"],
        ["abca"],
    ]:
        assert regex.accepts(test_case) == dfa.accepts(strs_to_word(test_case))


def test_epsilon_regex():
    regex, dfa = construct_regex_and_dfa("a$b$c")

    for test_case in [["abc"], ["a", "b", "c"], ["a", "", "b", "", "c"]]:
        assert regex.accepts(test_case) == dfa.accepts(strs_to_word(test_case))


def test_complex_regex():
    regex, dfa = construct_regex_and_dfa("(a+b)*(cc|$).d.e*")

    for test_case in [
        ["d"],
        ["a", "d"],
        ["a", "b", "d"],
        ["a", "a", "cc", "d", "e", "e"],
        ["ad"],
        ["a", "c", "d"],
        ["cc", "e"],
    ]:
        assert regex.accepts(test_case) == dfa.accepts(strs_to_word(test_case))
