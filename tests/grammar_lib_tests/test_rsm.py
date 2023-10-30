from project.grammar_lib import ecfg_of_file
from project.recursive_state_machine import rsm_of_ecfg, minimize_rsm
from project.extended_context_free_grammar import ECFG
from project.automaton_lib import dfa_of_regex
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex


def test_rsm_of_ecfg():
    source = "tests/test_grammars/1.ecfg"

    ecfg = ecfg_of_file(source)

    rsm = rsm_of_ecfg(ecfg)

    for start in rsm.subautomatons.keys():
        assert rsm.subautomatons[start].is_equivalent_to(
            ecfg.productions[start].to_epsilon_nfa()
        )

    assert rsm.starting_symbol == Variable("S")


def test_minimize_rsm():
    ecfg = ecfg_of_file("tests/test_grammars/3.ecfg")
    rsm = rsm_of_ecfg(ecfg)

    for start in ecfg.productions.keys():
        assert minimize_rsm(rsm).subautomatons[start] == dfa_of_regex(
            ecfg.productions[start]
        )
