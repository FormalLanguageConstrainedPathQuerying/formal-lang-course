from pyformlang.cfg import CFG, Variable


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