from pyformlang.cfg import cfg

LABEL: str = "label"
IS_FINAL: str = "is_final"
IS_START: str = "is_start"

LABELS_WITH_GREEKS: list[str] = ["a", "b", "c", "x", "y", "z", "alpha", "beta", "gamma"]
LABELS: list[str] = ["a", "b", "c", "d", "e", "f", "g", "h"]

REGEX_SIMPLE: list[str] = [
    "(aa)*",
    "a | a",
    "a* | a",
    "(ab) | (ac)",
    "(ab) | (abc)",
    "(abd) | (abc)",
    "(abd*) | (abc*)",
    "(abd)* | (abc)*",
    "((abd) | (abc))*",
    "a*a*",
    "a*a*b",
    "a* | (a | b)*",
    "a*(a | b)*",
    "(a | c)*(a | b)*",
]
REGEX_TUPLE: list[tuple[str, str]] = [
    ("a", "b"),
    ("a", "a"),
    ("a*", "a"),
    ("a*", "aa"),
    ("a*", "a*"),
    ("(aa)*", "a*"),
    ("(a|b)*", "a*"),
    ("(a|b)*", "b"),
    ("(a|b)*", "bbb"),
    ("a|b", "a"),
    ("a|b", "a|c"),
    ("(a|b)(c|d)", "(a|c)(b|d)"),
    ("(a|b)*", "(a|c)*"),
    ("a*b*", "(a|b)*"),
    ("(ab)*", "(a|b)*"),
]
QUERIES: list[str] = [
    "a",
    "a*",
    "ab",
    "abc",
    "abcd",
    "a*b*",
    "(ab)*",
    "ab*",
    "ab*c*",
    "ab*c",
    "abc*",
    "(a|b|c|d|e)*",
    "(a|b|c|d|e)(a|b|c|d|e)*",
    "(a|b|c|d|e)f*",
    "(a|b)*",
    "(a|b)*(c|d)*",
    "(a | b)*(c | d)*(e | f)*",
    "(a | b | c)*(d | e | f)*",
    "((a|b)*c)*",
    "((a | b) * c)*(d | e)",
    "((a | b)*c)*((d | e)*f)*",
]

REGEXP_CFG: dict[str, list[cfg.CFG]] = {
    "a": [cfg.CFG.from_text("S -> a"), cfg.CFG.from_text("S -> N B\nB -> $\nN -> a")],
    "a*": [
        cfg.CFG.from_text("S -> $ | a S"),
        cfg.CFG.from_text("S -> $ | S S | a"),
        cfg.CFG.from_text("S -> S a S | $"),
    ],
    "a b c": [cfg.CFG.from_text("S -> a b c"), cfg.CFG.from_text("S -> a B\nB -> b c")],
    "a*b*": [
        cfg.CFG.from_text("S -> S1 S2\nS2 -> $ | b S2\nS1 -> $ | a S1"),
        cfg.CFG.from_text("S -> $ | S1 | a S\nS1 -> $ | b S1"),
    ],
    "(a b)*": [
        cfg.CFG.from_text("S -> $ | a b S"),
        cfg.CFG.from_text("S -> $ | S S1\nS1 -> a b"),
    ],
    "a b*c*": [
        cfg.CFG.from_text("S -> S1 S2 S3\nS1 -> a\nS2 -> $ | S2 b\nS3 -> $ | c S3"),
        cfg.CFG.from_text("S -> a S2 S3\nS2 -> S2 b | $\nS3 -> c | $ | S3 S3"),
    ],
    "(a|b|c|d|e)*": [
        cfg.CFG.from_text("S -> $ | S1 S\nS1 -> a | b | c | d | e"),
        cfg.CFG.from_text("S -> $ | a | b | c | d | e | S S"),
        cfg.CFG.from_text("S -> $ | a S | b S | c S | e S | d S"),
    ],
    "((a | b) * c)*(d | e)": [
        cfg.CFG.from_text(
            "S -> S1 S2\nS1 -> S1 S1 | $ | S3 c\n S2 -> d | e\n S3 -> b S3 | $ | a S3"
        ),
        cfg.CFG.from_text("S -> S1 d | S1 e\nS1 -> S1 S3 c | $\nS3 -> b S3 | $ | a S3"),
    ],
}
GRAMMARS: list[list[cfg.CFG]] = [
    [
        cfg.CFG.from_text("S -> $ | a S b | S S"),
        cfg.CFG.from_text("S -> $ | a S b S"),
        cfg.CFG.from_text("S -> $ | S a S b"),
        cfg.CFG.from_text("S -> $ | a S b | S S S"),
    ],
    [
        cfg.CFG.from_text("S -> $ | a S b | c S d | S S"),
        cfg.CFG.from_text("S -> $ | a S b S | c S d S"),
        cfg.CFG.from_text("S -> $ | S a S b | S c S d"),
        cfg.CFG.from_text("S -> $ | a S b | c S d S | S S S"),
    ],
    [
        cfg.CFG.from_text("S -> $ | S1 S S2\nS1 -> a | c\n S2 -> b | d\n S -> S S"),
        cfg.CFG.from_text("S -> $ | S1 S S2 S\n S1 -> a | c\nS2 -> b | d"),
        cfg.CFG.from_text("S -> $ | S a S b | S a S d | S c S d | S c S b"),
        cfg.CFG.from_text("S -> $ | S1 S S2 | S S S\nS1 -> a | c\nS2-> b | d"),
    ],
    [
        cfg.CFG.from_text("S -> S S | Se S1 Se\nSe -> $ | Se e\nS1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> S1 | S S | e\nS1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> S2 S | $\n S2 -> e | S1\n S1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> $ | S1 S | e S\n S1 -> $ | a S1 b"),
    ],
    [
        cfg.CFG.from_text("S -> a S | $"),
        cfg.CFG.from_text("S -> S1 | a\nS1 -> a S1 | $"),
    ],
]
GRAMMARS_DIFFERENT: list[cfg.CFG] = [
    cfg.CFG.from_text(
        "S -> S1 | S2\nS1 -> Sab | S1 c\nSab -> $ | a Sab b\nS2 -> Sbc | a S2\nSbc -> b Sbc c"
    ),
    cfg.CFG.from_text("S -> a | b | S c S | S d S | e S f | g S"),
    cfg.CFG.from_text("S -> $ | a S b | b S a | e S f | S S | c S d | f S c | f S e"),
]
EBNF_GRAMMARS: list[str] = [
    """S -> ( Sab c* ) | ( a* Sbc )
    Sab -> a ( Sab | $ ) b
    Sbc -> b ( Sbc | $ ) c""",
    "S -> a | b | (S ( c | d ) S ) | ( e S f ) | ( g S )",
    "S -> ( ( a S b ) | ( b S a ) | ( c S d ) | ( d S c ) | ( e S f ) | (f S e) )*",
]
