from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA

from project.ecfg import ECFG


class RSM:
    def __init__(self, start: Variable, boxes: dict[Variable, EpsilonNFA]):
        self.start = start
        self.boxes = boxes

    @classmethod
    def from_ecfg(cls, ecfg: ECFG):
        return cls(
            ecfg.start,
            {head: body.to_epsilon_nfa() for head, body in ecfg.productions.items()},
        )

    def minimize(self) -> "RSM":
        for var, nfa in self.boxes.items():
            self.boxes[var] = nfa.minimize()
        return self
