from pyformlang.cfg import CFG, Variable, Production, Epsilon


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    cnf_cfg = cfg.to_normal_form()
    eps_els = cfg.get_nullable_symbols()
    productions = set(cnf_cfg.productions)
    for var in eps_els:
        productions.add(Production(Variable(var.value), [Epsilon()]))
    wcnf_cfg = CFG(
        start_symbol=cfg.start_symbol, productions=productions
    ).remove_useless_symbols()
    return wcnf_cfg
