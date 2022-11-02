from pyformlang.regular_expression import Regex
from pyformlang.cfg import CFG
from project.ecfg import ECFG


class ECFGManager:
    @staticmethod
    def create_from_cfg(cfg: CFG) -> ECFG:
        start_symbol = cfg.start_symbol
        productions = {}

        for production in cfg.productions:
            regex = Regex(
                ".".join(variable.value for variable in production.body)
                if len(production.body) > 0
                else ""
            )

            productions[production.head] = (
                productions[production.head].union(regex)
                if production.head in productions
                else regex
            )

        return ECFG(start_symbol, productions)
