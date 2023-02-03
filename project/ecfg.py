from pyformlang.cfg import Variable, Terminal, CFG
from pyformlang.regular_expression import Regex
from typing import Set, Dict


class ECFG:
    def __init__(
        self,
        variables: Set[Variable],
        terminals: Set[Terminal],
        productions: Dict[Variable, Regex],
        start: Variable,
    ):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start = start

    @classmethod
    def from_cfg(cls, cfg: CFG):
        if cfg.start_symbol is None:
            start_symbol = Variable("S")
        else:
            start_symbol = cfg.start_symbol

        variables = set(cfg.variables).union({start_symbol})

        productions: Dict[Variable, Regex] = {}
        for production in cfg.productions:
            if len(production.body) > 0:
                body = Regex(" ".join(symbol.value for symbol in production.body))
            else:
                body = Regex("$")
            # если у нескольких продукций одинаковая левая часть, то при порождении цепочек можем выбирать любую из
            # доступных правых частей, поэтому сформируем из группы продукций одну, объединив их правые части,
            # которые являются регулярными выражениями
            if production.head in productions:
                productions[production.head] = productions[production.head].union(body)
            else:
                productions[production.head] = body

        return cls(variables, set(cfg.terminals), productions, start_symbol)
