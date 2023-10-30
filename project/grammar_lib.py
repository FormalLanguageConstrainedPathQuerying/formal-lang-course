import re

from pyformlang.cfg import CFG, Variable, Terminal
from pyformlang.regular_expression import Regex

from project.extended_context_free_grammar import ECFG


def wcnf_of_cfg(cfg: CFG) -> CFG:
    """
    Converts context-free grammar into weakened cholmsky normal form.

    Context-free grammar is WCNF if and only if it consists of following rules:
    1. `S0 -> S1 S2`
    2. `S0 -> t`
    3. `S0 -> eps`
    Where `S0, S1, S2` are arbitrary non-terminals
          `t` is a terminal symbol
          `eps` is an empty sequence

    Args:
        cfg: context-free grammar to be converted

    Returns:
        weakened cholmsky normal form of cfg given

    """
    cfg = cfg.eliminate_unit_productions()
    cfg = cfg.remove_useless_symbols()
    new_productions = cfg._get_productions_with_only_single_terminals()
    new_productions = cfg._decompose_productions(new_productions)
    start_symbol = cfg.start_symbol
    return CFG(start_symbol=start_symbol, productions=set(new_productions))


def cfg_of_path(path: str, starting_symbol: str = "S") -> CFG:
    """
    Reads context-free grammar from file

    Args:
        path: path to the file to be read
        starting_symbol: starting symbol for created context-free grammar

    Returns:
        context-free grammar
    """
    with open(path) as file:
        source = file.read()

    return CFG.from_text(source, Variable(starting_symbol))


def ecfg_of_cfg(cfg: CFG) -> ECFG:
    """
    Converts context-free grammar to extended context-free grammar

    Args:
        cfg: context-free grammar to convert

    Returns:
        extended context-free grammar
    """
    ecfg_prods = {}

    for production in cfg.productions:
        if len(production.body) > 0:
            regex = Regex(".".join(variable.value for variable in production.body))
        else:
            regex = " "

        if production.head not in ecfg_prods:
            ecfg_prods[production.head] = regex
        else:
            ecfg_prods[production.head] = ecfg_prods[production.head].union(regex)

    return ECFG(cfg.variables, cfg.terminals, ecfg_prods, cfg.start_symbol)


def ecfg_of_string(source: str, starting_symbol: str = "S") -> ECFG:
    """
    Reads string containing productions for extended context-free grammar

    Args:
        source: source string of extended context-free grammar
        starting_symbol: starting symbol of ECFG, "S" by default

    Returns:
        extended context-free grammar
    """

    def remove_empty(lst):
        return list(filter(lambda x: x != "", lst))

    def extract_symbols(prod):
        non_symbols = "\[|\]|\(|\)|\||\+|\*|\?|\s"
        res = remove_empty(re.split(non_symbols, prod))
        if "epsilon" in res:
            res.remove("epsilon")
        return set(res)

    productions = dict()
    variables = set()
    terminals = set()

    for prod in source.split("\n"):
        prod = remove_empty(prod.strip().split())

        if len(prod) < 2:
            continue

        head = prod[0].strip()
        assert prod[1] == "->", '"->" missing in production'
        productions[head] = Regex(" ".join(prod[2::]))
        terminals = terminals.union(extract_symbols(" ".join(prod[2::])))
        variables.add(head)

    terminals = set(map(Terminal, terminals - variables))
    variables = set(map(Variable, variables))

    return ECFG(variables, terminals, productions, starting_symbol)


def ecfg_of_file(path: str, starting_symbol: str = "S") -> ECFG:
    """
    Reads extended context-free grammar from file

    Args:
        cfg: path to extended context-free grammar
        starting_symbol: starting symbol of ECFG, "S" by default

    Returns:
        extended context-free grammar
    """
    with open(path) as file:
        source = file.read()

    return ecfg_of_string(source, starting_symbol)
