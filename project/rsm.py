from typing import Dict

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from project.ecfg import ECFG


class RSM:
    def __init__(
        self, start: Variable, boxes: Dict[Variable, DeterministicFiniteAutomaton]
    ):
        self.start = start
        self.boxes = boxes

    @classmethod
    def from_ecfg(cls, ecfg: ECFG) -> "RSM":
        return cls(
            ecfg.start,
            {
                head: body.to_epsilon_nfa().to_deterministic()
                for head, body in ecfg.productions.items()
            },
        )

    def minimize(self) -> "RSM":
        for var, dfa in self.boxes.items():
            self.boxes[var] = dfa.minimize()
        return self
