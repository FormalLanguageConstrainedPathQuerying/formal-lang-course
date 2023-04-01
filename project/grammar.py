from pyformlang.cfg import CFG
from pyformlang.cfg import Variable


def cfg_from_file(file_name, start_symbol: str = "S") -> CFG:
    """
    Reading context-free grammar from file
    @param file_name:
    @param start_symbol:
    @return:
    """
    with open(file_name, "r") as file:
        text = file.read()
        return CFG.from_text(text, Variable(start_symbol))


def cfg_to_weak_cnf(cfg: CFG) -> CFG:
    """
    transform CFG to weak CNF
    @param cfg: input context free grammar
    @return: weak CNF of input grammar
    """
    cfg_eliminated_unit_prods_from = (
        cfg.eliminate_unit_productions().remove_useless_symbols()
    )
    single_term_cfg = (
        cfg_eliminated_unit_prods_from._get_productions_with_only_single_terminals()
    )
    productions = cfg_eliminated_unit_prods_from._decompose_productions(single_term_cfg)
    return CFG(start_symbol=cfg.start_symbol, productions=set(productions))
