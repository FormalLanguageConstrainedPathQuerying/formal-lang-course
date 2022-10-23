from pyformlang.cfg import CFG

__all__ = ["import_cfg_from_file", "from_cfg_to_weak_cnf"]


def import_cfg_from_file(path: str) -> CFG:
    with open(path) as f:
        content = f.readlines()
        return CFG.from_text("\n".join(content))


def from_cfg_to_weak_cnf(cfg: CFG) -> CFG:
    cfg_without_unit_productions = (
        cfg.eliminate_unit_productions().remove_useless_symbols()
    )
    new_productions = (
        cfg_without_unit_productions._get_productions_with_only_single_terminals()
    )
    new_productions = cfg_without_unit_productions._decompose_productions(
        new_productions
    )
    new_cfg = CFG(
        start_symbol=cfg_without_unit_productions.start_symbol,
        productions=set(new_productions),
    )
    return new_cfg
