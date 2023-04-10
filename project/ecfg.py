from pyformlang.cfg import CFG, Variable, Terminal
from project.rfa import RFA
from typing import AbstractSet, Dict
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(
        self,
        variables: AbstractSet[Variable] = None,
        terminals: AbstractSet[Terminal] = None,
        productions: Dict[Variable, Regex] = None,
        start_symbol: Variable = Variable("S"),
    ):
        self.variables = variables
        self.productions = productions
        self.start_symbol = start_symbol

    def from_cfg(cfg: CFG):
        productions = {}

        for prod in cfg.productions:
            regex = Regex(
                " ".join(
                    [x.to_text() for x in prod.body] if len(prod.body) > 0 else "$"
                )
            )

            if prod.head in productions:
                productions[prod.head] = productions[prod.head].union(regex)
            else:
                productions[prod.head] = regex

        return ECFG(
            cfg.variables,
            cfg.terminals,
            productions,
            cfg.start_symbol,
        )

    def from_text(text):
        variables = set()
        terminals = set()
        productions = {}

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            head_symbol, body_symbol = line.split("->")
            head = Variable(head_symbol.strip())
            variables.add(head)
            productions[head] = Regex(body_symbol)

        return ECFG(
            variables,
            {},
            productions,
        )

    def from_file(file):
        with open(file) as f:
            return from_text(f.read())

    def to_rfa(self):
        return RFA(
            start_symbol=self.start_symbol,
            dfas={
                k: v.to_epsilon_nfa().minimize() for k, v in self.productions.items()
            },
        )
