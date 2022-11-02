from pyformlang.cfg import Variable, Terminal, CFG
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(
        self,
        variables: set[Variable],
        terminals: set[Terminal],
        start: Variable,
        productions: dict[Variable, Regex],
    ):
        self.variables = variables
        self.terminals = terminals
        self.start = start
        self.productions = productions

    @classmethod
    def from_cfg(cls, cfg: CFG):
        variables = set(cfg.variables)

        if cfg.start_symbol is not None:
            start_symbol = cfg.start_symbol
        else:
            start_symbol = Variable("S")

        variables.add(start_symbol)

        productions: dict[Variable, Regex] = {}
        for p in cfg.productions:
            if len(p.body) > 0:
                body = Regex(" ".join(o.value for o in p.body))
            else:
                body = Regex("$")

            if p.head in productions:
                productions[p.head] = productions[p.head].union(body)
            else:
                productions[p.head] = body

        return cls(variables, set(cfg.terminals), start_symbol, productions)
