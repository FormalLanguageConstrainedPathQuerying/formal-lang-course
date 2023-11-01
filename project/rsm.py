from typing import Iterable
from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


class VariableFiniteAutomaton:
    """
    RSM can be represented as a set of finite automata for each nonterminal.
    This class is a finite automaton for a single nonterminal.
    """

    def __init__(self, variable: Variable, dfa: DeterministicFiniteAutomaton):
        self._variable = variable
        self._dfa = dfa

    def __eq__(self, other: "VariableFiniteAutomaton"):
        return self._variable == other._variable and self._dfa.is_equivalent_to(
            other._dfa
        )

    def minimize(self) -> None:
        self._dfa = self._dfa.minimize()

    @property
    def variables_finite_automata(self) -> Variable:
        return self._variable

    @property
    def dfa(self) -> DeterministicFiniteAutomaton:
        return self._dfa


class RSM:
    """
    This class is a recursive state machine (RSM) that can be represented as
    a set of finite automata for each nonterminal.
    """

    def __init__(
        self,
        start_variable: Variable,
        variables_finite_automata: Iterable[VariableFiniteAutomaton],
    ):
        self._start_variable = start_variable
        self._variables_finite_automata = variables_finite_automata

    def minimize(self) -> None:
        for variable_finite_automaton in self._variables_finite_automata:
            variable_finite_automaton.minimize()

    @property
    def start_variable(self) -> Variable:
        return self._start_variable

    @property
    def variables_finite_automata(self) -> Iterable[VariableFiniteAutomaton]:
        return self._variables_finite_automata
