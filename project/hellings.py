from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA
from scipy.sparse import dok_matrix

from project.my_cfg import ECFG


class RA:

    def __init__(self, start_symbol: Variable, boxes: dict[Variable, EpsilonNFA]):
        self.start_symbol: Variable = start_symbol
        self.boxes: dict[Variable, EpsilonNFA] = boxes

    def minimize(self):
        """
        Minimize automaton
        :return:
        """
        for variable, automate in self.boxes.items():
            self.boxes[variable] = automate.minimize()
        return self

    @classmethod
    def convert_ecfg(cls, ecfg: ECFG):
        """
        Create recursive automation from extended context-free grammar
        :param ecfg: original grammar
        :return: recursive automation of grammar
        """
        elements = {
            head: body.to_epsilon_nfa() for head, body in ecfg.ps.items()
        }
        return cls(ecfg.s_s, elements)

    def matrices(self):
        """
        Convert automath to adjacency matrix
        :return: dictionary of states indexes and dictionary of adjacency matrix by symbol
        """
        states = dict()
        matrix = dict()
        count = sum(len(item.states) for item in self.boxes.values())
        index = 0
        for variable, automath in self.boxes.items():
            for state in automath.states:
                states[(variable, state)] = index
                index += 1
            for start, symbol, end in automath:
                if symbol not in matrix:
                    matrix[symbol] = dok_matrix((count, count), dtype=bool)
                matrix[symbol][
                    states[(variable, start)], states[(variable, end)]
                ] = True

        return states, matrix
