from dataclasses import dataclass
from pyformlang.cfg import Variable
from project.extended_context_free_grammar import ECFG


@dataclass
class RSM:
    """
    Recursive state machine
    """

    variables: set
    terminals: set
    subautomatons: dict
    starting_symbol: Variable


def rsm_of_ecfg(ecfg: ECFG):
    """
    Creates recursive state machine of extended context-free grammar

    Args:
        ecfg: extended context-free grammar

    Returns:
        Recursive state machine built
    """
    subautomatons = {}

    for start, prod in ecfg.productions.items():
        subautomatons[start] = prod.to_epsilon_nfa()

    return RSM(ecfg.variables, ecfg.terminals, subautomatons, ecfg.starting_symbol)


def minimize_rsm(rsm: RSM):
    """
    Minimizes recursive state machine

    Args:
        rsm: Recursive state machine

    Returns:
        Minimized recursive state machine
    """
    subautomatons = {}

    for start, sub in rsm.subautomatons.items():
        subautomatons[start] = sub.minimize()

    return RSM(rsm.variables, rsm.terminals, subautomatons, rsm.starting_symbol)
