from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = ["RSMBox"]


class RSMBox:
    """
    A box for RMS

    Arguments
    ---------
    variable: Variable, default=None
        Variable for corresponding dfa
    dfa: DeterministicFiniteAutomaton, default=None
        DFA object
    """

    def __init__(
        self, variable: Variable = None, dfa: DeterministicFiniteAutomaton = None
    ):
        self._dfa = dfa
        self._variable = variable

    def __eq__(self, other: "RSMBox"):
        return self._variable == other._variable and self._dfa.is_equivalent_to(
            other._dfa
        )

    def minimize(self):
        """
        Minimize current RSMBox dfa

        Returns
        -------
        box: RSMBox
            RSMBox with minimized dfa
        """
        return RSMBox(variable=self._variable, dfa=self._dfa.minimize())

    @property
    def dfa(self):
        """
        Get dfa

        Returns
        -------
        dfa: DeterministicFiniteAutomaton
            self._dfa field
        """
        return self._dfa

    @property
    def variable(self):
        """
        Get variable

        Returns
        -------
        variable: Variable
            self._variable field
        """
        return self._variable
