from pyformlang.cfg import CFG


def cyk(cfg: CFG, str: str):
    if not str:
        return cfg.generate_epsilon()

    word_length = len(str)
    cnf = cfg.to_normal_form()
    dp = [[set() for _ in range(word_length)] for _ in range(word_length)]

    term_productions = [p for p in cnf.productions if len(p.body) == 1]
    var_productions = [p for p in cnf.productions if len(p.body) == 2]

    for i, c in enumerate(str):
        dp[i][i] = set(p.head for p in term_productions if p.body[0].value == c)

    for step in range(1, word_length):
        for i in range(word_length - step):
            j = i + step
            for k in range(i, j):
                dp[i][j] |= set(
                    p.head
                    for p in var_productions
                    if p.body[0] in dp[i][k] and p.body[1] in dp[k + 1][j]
                )

    return cfg.start_symbol in dp[0][word_length - 1]
