from typing import NamedTuple, Dict

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

__all__ = [
    "RSM",
]


class RSM(NamedTuple):
    """Class represents Recursive State Machine

    Attributes
    ----------

    start_symbol: Variable
        Start symbol of automaton
    boxes: Dict[Variable, DeterministicFiniteAutomaton]
        Mapping from variables to deterministic finite automatons
    """

    start_symbol: Variable
    boxes: Dict[Variable, DeterministicFiniteAutomaton]

    def minimize(self) -> "RSM":
        """Minimizes RSM by minimizing internal automatons

        Returns
        -------
        minimized_rsm : RSM
            Minimized recursive state machine
        """
        return RSM(
            start_symbol=self.start_symbol,
            boxes={v: a.minimize() for v, a in self.boxes.items()},
        )
