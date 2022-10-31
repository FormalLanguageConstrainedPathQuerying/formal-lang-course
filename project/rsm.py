from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from project.ecfg import ECFG


class RSM:
    def __init__(
        self,
        start_symbol: Variable,
        boxes: dict[Variable, DeterministicFiniteAutomaton],
    ):
        self.start_symbol = start_symbol
        self.boxes = boxes

    @classmethod
    def ecfg_to_rsm(cls, ecfg: ECFG):
        boxes = dict()
        for key, value in ecfg.productions.items():
            boxes[key] = value.to_epsilon_nfa().to_deterministic()
        return cls(ecfg.start_symbol, boxes)

    def minimize(self):
        for key, value in self.boxes.items():
            self.boxes[key] = value.minimize()
        return self
