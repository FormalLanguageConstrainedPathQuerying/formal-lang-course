from pyformlang.cfg import CFG, Variable
from pyformlang.finite_automaton import EpsilonNFA
from project.graph_regular_query import fa2matrix
from typing import Dict


class RFA:
    """
    Recursive finite automaton
    """

    def __init__(self, start_symbol: Variable, dfas: Dict[Variable, EpsilonNFA]):
        self.start_symbol = start_symbol
        self.dfas = dfas

    def minimize(self):
        """
        Minimize the automaton

        Returns:
            Minimized RFA
        """
        return RFA(self.start_symbol, {v: fa.minimize() for v, fa in self.dfas.items()})

    def to_matrices(self):
        """
        Builds a dictionary of matrices for a given RFA

        Returns:
            Dictionary from state to matrices, generated by fa2matrix
        """
        return {v: fa2matrix(dfa) for v, dfa in self.dfas.items()}
