from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA

from project.ecfg import ECFG


class RecursiveAutomata:
    def __init__(
        self,
        start_variable: Variable,
        variable_to_automata: list[tuple[Variable, EpsilonNFA]],
    ):
        self._start_variable = start_variable
        self._variable_to_automata = variable_to_automata

    def minimize(self) -> "RecursiveAutomata":
        return RecursiveAutomata(
            self._start_variable,
            [(v, nfa.minimize()) for v, nfa in self._variable_to_automata],
        )

    @classmethod
    def from_ecfg(cls, ecfg: ECFG) -> "RecursiveAutomata":
        return RecursiveAutomata(
            ecfg.start_variable,
            [(v, regex.to_epsilon_nfa()) for v, regex in ecfg.productions.items()],
        )
