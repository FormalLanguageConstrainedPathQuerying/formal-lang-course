import pyformlang.cfg
from pyformlang.cfg import CFG
from pyformlang.cfg import Variable
from pyformlang.cfg import Terminal
from pyformlang.regular_expression import Regex


def cfg_from_file(file_name, start_symbol: str = "S") -> CFG:
    """
    Reading context-free grammar from file
    @param file_name: name of file to read from
    @param start_symbol: str with start symbol (default 'S')
    @return: context-free grammar read from file
    """
    with open(file_name, "r") as file:
        text = file.read()
        return CFG.from_text(text, Variable(start_symbol))


def cfg_to_weak_cnf(cfg: CFG) -> CFG:
    """
    transform CFG to weak CNF
    @param cfg: input context free grammar
    @return: weak CNF of input grammar
    """
    cfg_eliminated_unit_prods_from = (
        cfg.eliminate_unit_productions().remove_useless_symbols()
    )
    single_term_cfg = (
        cfg_eliminated_unit_prods_from._get_productions_with_only_single_terminals()
    )
    productions = cfg_eliminated_unit_prods_from._decompose_productions(single_term_cfg)
    return CFG(start_symbol=cfg.start_symbol, productions=set(productions))


class ExtendedContextFreeGrammars:
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
        terminals = set(cfg.terminals)
        start_symbol = cfg.start_symbol if cfg.start_symbol else Variable("S")
        variables.add(start_symbol)

        productions: dict[Variable, Regex] = {}
        for production in cfg.productions:
            if len(production.body) > 0:
                reg = Regex(" ".join(o.value for o in production.body))
            else:
                reg = Regex("$")
            if production.head in productions:
                productions[production.head] = productions[production.head].union(reg)
            else:
                productions[production.head] = reg
        return cls(variables, terminals, start_symbol, productions)
