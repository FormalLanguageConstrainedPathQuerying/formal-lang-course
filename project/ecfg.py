from typing import AbstractSet, Iterable
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

from project.automaton_utils import regex_to_dfa
from project.rsm import RSMBox, RSM


class ECFGProduction:
    """
    This class represents a production of a ECFG
    """

    def __init__(self, head: Variable, body: Regex):
        self._head = head
        self._body = body

    def __str__(self):
        return str(self._head) + " -> " + str(self._body)

    @property
    def head(self) -> Variable:
        return self._head

    @property
    def body(self) -> Regex:
        return self._body


class InvalidECFGException(Exception):
    """
    This class represents an Extended CFG.
    Extended CFG:
        - There is exactly one rule for each nonterminal.
        - One line contains exactly one rule.
        - the rule is a nonterminal and regex over terminals and nonterminals accepted by pyformlang and separated by '->'.
          For example: S -> a | b * S
    """

    def __init__(self, message: str):
        self.message = message


class ECFG:
    """
    This class represents an Extended CFG.
    Extended CFG:
        - There is exactly one rule for each nonterminal.
        - One line contains exactly one rule.
        - the rule is a nonterminal and regex over terminals and nonterminals accepted by pyformlang and separated by '->'.
          For example: S -> a | b * S
    """

    def __init__(
        self,
        variables: AbstractSet[Variable],
        start_variable: Variable,
        productions: Iterable[ECFGProduction],
    ):
        self._variables = variables
        self._start_variable = start_variable
        self._productions = productions

    @property
    def variables(self) -> AbstractSet[Variable]:
        return self._variables

    @property
    def productions(self) -> AbstractSet[ECFGProduction]:
        return self._productions

    @property
    def start_variable(self) -> Variable:
        return self._start_variable

    def to_text(self) -> str:
        return "\n".join(str(production) for production in self._productions)

    @staticmethod
    def from_text(text: str, start_variable=Variable("S")) -> "ECFG":
        variables = set()
        productions = set()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            production_objects = line.split("->")
            if len(production_objects) != 2:
                raise InvalidECFGException(
                    "There should be only one production on each line."
                )

            head_text, body_text = production_objects
            head = Variable(head_text.strip())
            if head in variables:
                raise InvalidECFGException(
                    "There should be strictly one production for each nonterminal."
                )
            variables.add(head)
            body = Regex(body_text.strip())
            productions.add(ECFGProduction(head, body))

        return ECFG(variables, start_variable, productions)

    @staticmethod
    def from_file(path: str, start_variable: str = "S") -> "ECFG":
        with open(path) as file:
            return ECFG.from_text(file.read(), Variable(start_variable))


def ecfg_to_rsm(ecfg: ECFG) -> RSM:
    automata = [
        RSMBox(production.head, regex_to_dfa(production.body))
        for production in ecfg.productions
    ]
    return RSM(ecfg.start_variable, automata)
