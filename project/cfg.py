from os import PathLike
import pyformlang.cfg as c


def cfg_to_wcnf(cfg: str | c.CFG, start: str = "S") -> c.CFG:
    if not isinstance(cfg, c.CFG):
        cfg = c.CFG.from_text(cfg, c.Variable(start))
    cleared_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )
    cleared_productions = cleared_cfg._get_productions_with_only_single_terminals()
    cleared_productions = cleared_cfg._decompose_productions(cleared_productions)
    return c.CFG(start_symbol=cfg._start_symbol, productions=set(cleared_productions))


def read_cfg(path: PathLike, start: str = "S") -> c.CFG:
    with open(path, "r") as f:
        data = f.read()
    return c.CFG.from_text(data, c.Variable(start))
