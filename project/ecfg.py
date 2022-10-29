from pyformlang.cfg import Variable, CFG
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(self, start_variable: Variable, productions: dict[Variable, Regex]):
        self._start_variable = start_variable
        assert start_variable in productions
        self._productions = productions

    @property
    def start_variable(self):
        return self._start_variable

    @property
    def productions(self):
        return self._productions

    @classmethod
    def from_pyformlang_cfg(cls, cfg: CFG) -> "ECFG":
        start_variable = cfg.start_symbol
        productions = dict()
        for production in cfg.productions:
            if production.head not in productions:
                productions[production.head] = Regex("")
            body = Regex(
                ".".join(symbol.value for symbol in production.body)
                if len(production.body) > 0
                else "$"
            )
            productions[production.head].union(body)
        return ECFG(start_variable, productions)
