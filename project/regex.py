from pyformlang.regular_expression import Regex
from project.automaton_utils import regex_to_dfa


def check_regex_equality(r1: Regex, r2: Regex):
    return regex_to_dfa(r1).is_equivalent_to(regex_to_dfa(r2))
