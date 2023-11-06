import re
from typing import Optional

from pyformlang.cfg import CFG, Variable, Terminal, Epsilon
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph

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


def hellings_path_query(
    graph: MultiDiGraph,
    request: CFG,
    start_nodes: Optional[set] = None,
    final_nodes: Optional[set] = None,
):
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes

    wcnf = wcnf_of_cfg(request)

    eps_prods = set()
    term_prods = dict()
    var_prods = dict()

    for prod in wcnf.productions:
        # S -> eps
        if len(prod.body) == 0:
            eps_prods.add(prod.head)
            continue

        if prod.body[0].__class__ is Terminal:
            terminal = prod.body[0]
            if prod.head not in term_prods.keys():
                term_prods[prod.head] = set()
            term_prods[prod.head].add(terminal)
            continue

        if prod.body[0].__class__ is Variable:
            fst = prod.body[0]
            snd = prod.body[1]
            if prod.head not in var_prods.keys():
                var_prods[prod.head] = set()
            var_prods[prod.head] = (fst, snd)
            continue

    result = set()

    for node in graph.nodes:
        for var in eps_prods:
            result.add((node, var, node))

    for fst, snd, label in graph.edges.data("label"):
        for var in term_prods:
            if Terminal(label) in term_prods[var]:
                result.add((fst, var, snd))

    remaining = result.copy()

    while len(remaining) != 0:
        fst_start, fst_var, fst_end = remaining.pop()

        for snd_start, snd_var, snd_end in result:
            if fst_start == snd_end:
                for var in var_prods:
                    if (snd_var, fst_var) not in var_prods[var]:
                        continue

                    if (snd_start, var, fst_start) in result:
                        continue

                    remaining.add((snd_start, var, fst_end))
                    result.add((snd_start, var, fst_end))

            if snd_start == fst_end:
                for var in var_prods:
                    if (fst_var, snd_var) not in var_prods[var]:
                        continue

                    if (fst_start, var, snd_end) in result:
                        continue

                    remaining.add((fst_start, var, snd_end))
                    result.add((fst_start, var, snd_end))

    final_result = set()

    for start_node, var, final_node in result:
        if start_node == "\n" or final_node == "\n":
            continue

        if start_node not in start_nodes:
            continue

        if final_node not in final_nodes:
            continue

        if var != request.start_symbol:
            continue

        final_result.add((start_node, final_node))

    return final_result
