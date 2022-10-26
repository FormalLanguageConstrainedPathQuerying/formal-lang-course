from pyformlang.cfg import CFG


class CFGManager:
    @staticmethod
    def read_cfg_from_file(path: str) -> CFG:
        with open(path) as file:
            return CFG.from_text(file.read())

    @staticmethod
    def convert_cfg_to_wcnf(cfg: CFG) -> CFG:
        clean_cfg = (
            cfg.remove_useless_symbols()
            .eliminate_unit_productions()
            .remove_useless_symbols()
        )

        productions_with_only_single_terminals = (
            clean_cfg._get_productions_with_only_single_terminals()
        )
        decomposed_productions = clean_cfg._decompose_productions(
            productions_with_only_single_terminals
        )

        return CFG(
            start_symbol=clean_cfg.start_symbol, productions=set(decomposed_productions)
        )
