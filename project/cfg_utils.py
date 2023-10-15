import os
from pyformlang.cfg import CFG


def cfg_to_wcnf(cfg: CFG) -> CFG:
    wcnf = cfg.eliminate_unit_productions().remove_useless_symbols()
    new_productions = wcnf._get_productions_with_only_single_terminals()
    new_productions = wcnf._decompose_productions(new_productions)
    return CFG(start_symbol=wcnf.start_symbol, productions=set(new_productions))


def cfg_from_file(file_path: str, start_symbol: str = "S") -> CFG:
    _check_path(file_path)
    with open(file_path, "r") as file:
        cfg_str = file.read()
    return CFG.from_text(cfg_str, start_symbol)


def _check_path(path: str) -> None:
    if not os.path.exists(path):
        raise OSError("Error: specified file does not exist.")
    if os.path.getsize(path) == 0:
        raise OSError("Error: specified file is empty.")


def is_wcnf(cfg: CFG) -> bool:
    for production in cfg.productions:
        body = production.body
        if not (
            # (1) S -> A B, where S, A, B in Variables:
            (len(body) <= 2 and all(map(lambda x: x in cfg.variables, body)))
            # (2) S -> t, where S in Variables, t in Terminals:
            or (len(body) == 1 and body[0] in cfg.terminals)
            # (3) S -> epsilon, where S in Variables:
            or (not body)
        ):
            return False
    return True


def check_epsilon_equivalence(cfg_new: CFG, cfg_old: CFG) -> bool:
    productions_old_with_epsilon = set(
        filter(
            lambda production: production.head in cfg_new.variables
            and not production.body,
            cfg_old.productions,
        )
    )
    productions_new_with_epsilon = set(
        filter(lambda production: not production.body, cfg_new.productions)
    )
    for production in productions_old_with_epsilon:
        if production not in productions_new_with_epsilon:
            return False
    return True
