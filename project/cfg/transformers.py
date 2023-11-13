from pyformlang.cfg import CFG


def transform_to_wcnf(cfg: CFG) -> CFG:
    """Transforms a CFG to the Weak Chomsky Normal Form
    if possible without transform to Chomsky Normal Form

    Returns
    ----------
    new_cfg : CFG
        A new CFG equivalent in the WCNF form

    """
    new_cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    new_productions = new_cfg._decompose_productions(
        new_cfg._get_productions_with_only_single_terminals()
    )
    return CFG(start_symbol=new_cfg.start_symbol, productions=set(new_productions))
