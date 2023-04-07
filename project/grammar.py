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


class ECFG:
    """
    Extended context free grammars
    """

    class ECFGException(RuntimeError):
        pass

    def __init__(
        self,
        variables: set[Variable],
        terminals: set[Terminal],
        start: Variable,
        productions: dict[Variable, Regex],
    ):
        """
        Initialising Extended context free grammar
        @param variables: set of Non-terminal sybmols
        @param terminals: set of terminal symbols
        @param start: start Variable
        @param productions: dictionary of rules like: 'A -> Regex(" a | b* S ")'
        """
        self.variables = variables
        self.terminals = terminals
        self.start = start
        self.productions = productions

    def __getitem__(self, item):
        return self.productions[item]

    @classmethod
    def from_string(cls, string: str, start: Variable = Variable("S")):
        """
        Reads ecfg from string to ECFG
        :param string: text with ecfg
        :param start: start Variable
        :return: ECFG
        """
        variables = set()
        terminals = set()
        productions_dict = {}
        for line in string.splitlines():
            line = line.strip()
            if not line:
                continue
            productions = line.split("->")
            if len(productions) != 2:
                raise cls.ECFGException(f"Illegal production: {repr(line)}")
            head_text, body_text = productions
            head = Variable(head_text.strip())
            if head in variables:
                raise cls.ECFGException(f"Variable {head} appears more than once")
            variables.add(head)
            regex = Regex(body_text)

            def get_sons(regexable):
                if len(regexable.sons) > 0:
                    res = set()
                    for son in regexable.sons:
                        res = res.union(get_sons(son))
                    return res
                else:
                    return {regexable.head.value}

            terminals.update(get_sons(regex))
            productions_dict[head] = regex
        terminals = set(filter(lambda t: t not in variables, terminals))
        return ECFG(variables, terminals, start, productions_dict)

    @classmethod
    def from_file(cls, filename):
        """
        Reads ecfg from file
        @param filename: name of file
        @return: ECFG
        """
        with open(filename) as f:
            return cls.from_string(f.read())


def ecfg_from_cfg(cfg: CFG):
    """
    Transform context free grammar to extended context free grammars
    @param cfg: context free grammar for converts
    @return: extended context free grammars
    """
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
    return ECFG(variables, terminals, start_symbol, productions)
