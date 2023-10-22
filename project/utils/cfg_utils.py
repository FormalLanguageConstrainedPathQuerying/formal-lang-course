from pyformlang.cfg import CFG


def read_cfg(path: str, start_symbol: str = "S") -> CFG:
    with open(path, "r") as f:
        cfg_in_text = f.read()
    cfg = CFG.from_text(cfg_in_text, start_symbol)
    return cfg


def cfg_to_wcnf(cfg: CFG):
    cfg_min = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    new_productions = cfg_min._decompose_productions(
        cfg_min._get_productions_with_only_single_terminals()
    )

    cnf = CFG(start_symbol=cfg.start_symbol, productions=set(new_productions))
    return cnf
