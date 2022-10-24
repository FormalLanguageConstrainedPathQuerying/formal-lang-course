from pyformlang.cfg import CFG


def to_wcnf(cfg: CFG) -> CFG:
    cfg_new = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    new_productions = cfg_new._get_productions_with_only_single_terminals()
    new_productions = cfg_new._decompose_productions(new_productions)
    return CFG(start_symbol=cfg_new.start_symbol, productions=set(new_productions))


def read_cfg_from_text(path_to_file) -> CFG:
    with open(path_to_file, "r") as file:
        cfg_string = file.read()
    return CFG.from_text(cfg_string)
