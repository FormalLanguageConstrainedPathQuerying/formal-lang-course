from os import PathLike
from typing import Union

from pyformlang.cfg import CFG
from pyformlang.cfg import Variable


def cfg_to_wcnf(cfg: Union[CFG, str], starting: str = "S") -> CFG:
    if isinstance(cfg, str):
        cfg = CFG.from_text(cfg, Variable(starting))

    # По записям в моих конспектах единственное отличие в преобразовании CFG к WCNF в сравнении с
    # преобразованием CFG к CNF заключается в отсутствии того шага, на котором устраняются эпсилон-продукции.

    # Заимствуем код из pyformlang метода CFG.to_normal_form()
    new_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    new_productions = new_cfg._get_productions_with_only_single_terminals()
    new_productions = new_cfg._decompose_productions(new_productions)

    cfg_in_wcnf = CFG(start_symbol=cfg._start_symbol, productions=set(new_productions))

    return cfg_in_wcnf


def read_cfg(path: PathLike, starting: str = "S") -> CFG:
    with open(path, "r") as f:
        data = f.read()
    return CFG.from_text(data, Variable(starting))
