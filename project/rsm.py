from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA

from project.grammar import ECFG


class RSM:
    def __init__(
        self, nfa_dict: dict[Variable, EpsilonNFA], start: Variable = Variable("S")
    ):
        self.nfa_dict = nfa_dict
        self.start = start

    def minimize(self) -> "RSM":
        min_nfa_dict: dict[Variable, EpsilonNFA] = {}
        for var, nfa in self.nfa_dict.items():
            min_nfa_dict[var] = nfa.minimize()
        return RSM(min_nfa_dict, self.start)


def rsm_from_ecfg(ecfg: ECFG):
    nfa_dict: dict[Variable, EpsilonNFA] = {}
    for var, reg in ecfg.productions.items():
        nfa_dict[var] = reg.to_epsilon_nfa()
    return RSM(nfa_dict, ecfg.start)
