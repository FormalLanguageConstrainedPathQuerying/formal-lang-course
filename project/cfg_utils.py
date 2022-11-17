from pyformlang.cfg import CFG, Terminal

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


def check_word_in_cfg_language(cfg: CFG, word: str) -> bool:
    if len(word) == 0:
        return cfg.generate_epsilon()

    # initializing
    cfg = cfg.to_normal_form()
    dp = dict()
    for production in cfg.productions:
        if production.head not in dp:
            dp[production.head] = dict()
            for i in range(len(word)):
                dp[production.head][i] = dict()
                for j in range(len(word)):
                    dp[production.head][i][j] = False

    word = [Terminal(c) for c in word]
    for i in range(len(word)):
        for production in cfg.productions:
            if len(production.body) == 1 and production.body[0] == word[i]:
                dp[production.head][i][i] = True

    # CYK algorithm
    for m in range(1, len(word)):
        for production in cfg.productions:
            for i in range(len(word) - m):
                for k in range(0, m + 1):
                    if len(production.body) == 2:
                        dp[production.head][i][i + m] = dp[production.head][i][
                            i + m
                        ] or (
                            dp[production.body[0]][i][i + k]
                            and dp[production.body[1]][i + k + 1][i + m]
                        )

    return dp[cfg.start_symbol][0][len(word) - 1]
