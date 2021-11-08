from pyformlang.cfg import CFG

__all__ = ["cyk"]


def cyk(cfg: CFG, word: str) -> bool:
    """
    Cocke-Younger-Kasami algorithm implementation.
    Check whether CFG accepts given word

    Parameters
    ----------
    cfg: CFG
        Context Free Grammar
    word: str
        Word to check acceptance

    Returns
    -------
    is_accepted: bool
        True if CFG accepts word, False otherwise
    """
    word_len = len(word)

    if not word_len:
        return cfg.generate_epsilon()

    cnf = cfg.to_normal_form()

    term_productions = [p for p in cnf.productions if len(p.body) == 1]
    var_productions = [p for p in cnf.productions if len(p.body) == 2]

    m = [[set() for _ in range(word_len)] for _ in range(word_len)]

    for i in range(word_len):
        m[i][i].update(
            production.head.value
            for production in term_productions
            if word[i] == production.body[0].value
        )

    for step in range(1, word_len):
        for i in range(word_len - step):
            j = i + step
            for k in range(i, j):
                m[i][j].update(
                    production.head.value
                    for production in var_productions
                    if production.body[0].value in m[i][k]
                    and production.body[1].value in m[k + 1][j]
                )
    return cnf.start_symbol.value in m[0][word_len - 1]
