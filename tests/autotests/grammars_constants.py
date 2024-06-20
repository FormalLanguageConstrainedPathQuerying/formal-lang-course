from pyformlang.cfg import cfg
from constants import *
from random import sample

GRAMMARS_TABLE: list[dict[str, list[str | cfg.CFG]]] = [
    {
        REGEXP: ["(a | b | c)*(d | e | f)*"],
        CFG: [],
        EBNF: ["S -> (a | b | c)*(d | e | f)*"],
    },
    {REGEXP: ["(a b) | (a c)"], CFG: [], EBNF: ["S -> (a b) | (a c)"]},
    {REGEXP: ["a b c*"], CFG: [], EBNF: ["S -> a b c*"]},
    {REGEXP: ["(a b d) | (a b c)"], CFG: [], EBNF: ["S -> (a b d) | (a b c)"]},
    {
        REGEXP: ["(a|b|c|d|e)(a|b|c|d|e)*"],
        CFG: [],
        EBNF: ["S -> (a|b|c|d|e)(a|b|c|d|e)*"],
    },
    {REGEXP: ["(a|b)*(c|d)*"], CFG: [], EBNF: ["S -> (a|b)*(c|d)*"]},
    {REGEXP: ["(a|b|c|d|e)f*"], CFG: [], EBNF: ["S -> (a|b|c|d|e)f*"]},
    {REGEXP: ["a a"], CFG: [], EBNF: ["S -> a a"]},
    {REGEXP: ["a b*"], CFG: [], EBNF: ["S -> a b*"]},
    {REGEXP: ["a b"], CFG: [], EBNF: ["S -> a b"]},
    {REGEXP: ["(a b) | (a b c)"], CFG: [], EBNF: ["S -> (a b) | (a b c)"]},
    {REGEXP: ["a|c"], CFG: [], EBNF: ["S -> a|c"]},
    {REGEXP: ["(a|c)(b|d)"], CFG: [], EBNF: ["S -> (a|c)(b|d)"]},
    {REGEXP: ["b"], CFG: [cfg.CFG.from_text("S -> b")], EBNF: ["S -> b"]},
    {REGEXP: ["a*a*b"], CFG: [], EBNF: ["S -> a*a*b"]},
    {
        REGEXP: ["((a | b)*c)*((d | e)*f)*"],
        CFG: [],
        EBNF: ["S -> ((a | b)*c)*((d | e)*f)*"],
    },
    {REGEXP: ["((a b d) | (a b c))*"], CFG: [], EBNF: ["S -> ((a b d) | (a b c))*"]},
    {REGEXP: ["(a|c)*"], CFG: [], EBNF: ["S -> (a|c)*"]},
    {REGEXP: ["(a | c)*(a | b)*"], CFG: [], EBNF: ["S -> (a | c)*(a | b)*"]},
    {
        REGEXP: ["(a | b)*(c | d)*(e | f)*"],
        CFG: [],
        EBNF: ["S -> (a | b)*(c | d)*(e | f)*"],
    },
    {
        REGEXP: ["a*(a | b)*", "(a|b)*", "a* | (a | b)*"],
        CFG: [],
        EBNF: ["S -> a*(a | b)*"],
    },
    {REGEXP: ["(a b d)* | (a b c)*"], CFG: [], EBNF: ["S -> (a b d)* | (a b c)*"]},
    {REGEXP: ["a b* c"], CFG: [], EBNF: ["S -> a b* c"]},
    {REGEXP: ["(a a)*"], CFG: [], EBNF: ["S -> (a a)*"]},
    {REGEXP: ["((a|b)*c)*"], CFG: [], EBNF: ["S -> ((a|b)*c)*"]},
    {REGEXP: ["a b c d"], CFG: [], EBNF: ["S -> a b c d"]},
    {
        REGEXP: [
            "b b b",
        ],
        CFG: [],
        EBNF: [
            "S -> b b b",
        ],
    },
    {REGEXP: ["(a b d*) | (a b c*)"], CFG: [], EBNF: ["S -> (a b d*) | (a b c*)"]},
    {
        REGEXP: ["a", "a | a"],
        CFG: [
            cfg.CFG.from_text("S -> a"),
            cfg.CFG.from_text(
                """
                S -> N B
                B -> $
                N -> a
                """
            ),
        ],
        EBNF: ["S -> a"],
    },
    {
        REGEXP: ["a*", "a* a*", "a* | a"],
        CFG: [
            cfg.CFG.from_text("S -> $ | a S"),
            cfg.CFG.from_text("S -> $ | S S | a"),
            cfg.CFG.from_text("S -> S a S | $"),
        ],
        EBNF: ["S -> a*"],
    },
    {
        REGEXP: ["a b c"],
        CFG: [
            cfg.CFG.from_text("S -> a b c"),
            cfg.CFG.from_text(
                """
                S -> a B
                B -> b c
                """
            ),
        ],
        EBNF: ["S -> a b c"],
    },
    {
        REGEXP: ["a*b*"],
        CFG: [
            cfg.CFG.from_text(
                """
                S -> S1 S2
                S2 -> $ | b S2
                S1 -> $ | a S1
                """
            ),
            cfg.CFG.from_text(
                """
                S -> $ | S1 | a S
                S1 -> $ | b S1
                """
            ),
        ],
        EBNF: ["S -> a*b*"],
    },
    {
        REGEXP: ["(a b)*"],
        CFG: [
            cfg.CFG.from_text("S -> $ | a b S"),
            cfg.CFG.from_text(
                """
                S -> $ | S S1
                S1 -> a b
                """
            ),
        ],
        EBNF: ["S -> (a b)*"],
    },
    {
        REGEXP: ["a b*c*"],
        CFG: [
            cfg.CFG.from_text(
                """
                S -> S1 S2 S3
                S1 -> a
                S2 -> $ | S2 b
                S3 -> $ | c S3
                """
            ),
            cfg.CFG.from_text(
                """
                S -> a S2 S3
                S2 -> S2 b | $
                S3 -> c | $ | S3 S3
                """
            ),
        ],
        EBNF: ["S -> a b*c*"],
    },
    {
        REGEXP: ["(a|b|c|d|e)*"],
        CFG: [
            cfg.CFG.from_text(
                """
                S -> $ | S1 S
                S1 -> a | b | c | d | e
                """
            ),
            cfg.CFG.from_text("S -> $ | a | b | c | d | e | S S"),
            cfg.CFG.from_text("S -> $ | a S | b S | c S | e S | d S"),
        ],
        EBNF: ["S -> (a|b|c|d|e)*"],
    },
    {
        REGEXP: ["((a | b) * c)*(d | e)"],
        CFG: [
            cfg.CFG.from_text(
                """
                S -> S1 S2
                S1 -> S1 S1 | $ | S3 c
                S2 -> d | e
                S3 -> b S3 | $ | a S3
                """
            ),
            cfg.CFG.from_text(
                """
                S -> S1 d | S1 e
                S1 -> S1 S3 c | $
                S3 -> b S3 | $ | a S3
                """
            ),
        ],
        EBNF: ["S -> ((a | b) * c)*(d | e)"],
    },
    {
        REGEXP: [],
        CFG: [
            cfg.CFG.from_text("S -> $ | a S b | S S"),
            cfg.CFG.from_text("S -> $ | a S b S"),
            cfg.CFG.from_text("S -> $ | S a S b"),
            cfg.CFG.from_text("S -> $ | a S b | S S S"),
        ],
        EBNF: ["S -> $ | a S b | S S"],
    },
    {
        REGEXP: [],
        CFG: [
            cfg.CFG.from_text("S -> $ | a S b | c S d | S S"),
            cfg.CFG.from_text("S -> $ | a S b S | c S d S"),
            cfg.CFG.from_text("S -> $ | S a S b | S c S d"),
            cfg.CFG.from_text("S -> $ | a S b | c S d S | S S S"),
        ],
        EBNF: ["S -> $ | a S b | c S d | S S"],
    },
    {
        REGEXP: [],
        CFG: [
            cfg.CFG.from_text(
                """
                S -> $ | S1 S S2 | S S
                S1 -> a | c
                S2 -> b | d
                """
            ),
            cfg.CFG.from_text(
                """
                S -> $ | S1 S S2 S
                S1 -> a | c
                S2 -> b | d
                """
            ),
            cfg.CFG.from_text("S -> $ | S a S b | S a S d | S c S d | S c S b"),
            cfg.CFG.from_text(
                """
                S -> $ | S1 S S2 | S S S
                S1 -> a | c
                S2-> b | d
                """
            ),
        ],
        EBNF: ["S -> $ | S a S b | S a S d | S c S d | S c S b"],
    },
    {
        REGEXP: [],
        CFG: [
            cfg.CFG.from_text(
                """
                S -> S S | Se S1 Se
                Se -> $ | Se e
                S1 -> $ | a S1 b
                """
            ),
            cfg.CFG.from_text(
                """
                S -> S1 | S S | e
                S1 -> $ | a S1 b
                """
            ),
            cfg.CFG.from_text(
                """
                S -> S2 S | $
                S2 -> e | S1
                S1 -> $ | a S1 b
                """
            ),
            cfg.CFG.from_text(
                """
                S -> $ | S1 S | e S
                S1 -> $ | a S1 b
                """
            ),
        ],
        EBNF: [
            """
            S -> S1 | S S | e
            S1 -> $ | a S1 b
            """
        ],
    },
    {
        REGEXP: [],
        CFG: [
            cfg.CFG.from_text("S -> a S | $"),
            cfg.CFG.from_text(
                """
                S -> S1 | a
                S1 -> a S1 | $
                """
            ),
        ],
        EBNF: ["S -> a S | $"],
    },
    {
        REGEXP: [],
        CFG: [
            cfg.CFG.from_text(
                """
                S -> S1 | S2
                S1 -> Sab | S1 c
                Sab -> $ | a Sab b
                S2 -> Sbc | a S2
                Sbc -> $ | b Sbc c
                """
            )
        ],
        EBNF: [
            """
            S -> ( Sab c* ) | ( a* Sbc ) | $
            Sab -> a Sab b | $
            Sbc -> b Sbc c | $
            """
        ],
    },
    {
        REGEXP: [],
        CFG: [cfg.CFG.from_text("S -> a | b | S c S | S d S | e S f | g S")],
        EBNF: ["S -> a | b | (S ( c | d ) S ) | ( e S f ) | ( g S )"],
    },
    {
        REGEXP: [],
        CFG: [
            cfg.CFG.from_text(
                "S -> $ | a S b | b S a | e S f | S S | c S d | d S c | f S e"
            ),
        ],
        EBNF: [
            "S -> ( ( a S b ) | ( b S a ) | ( c S d ) | ( d S c ) | ( e S f ) | (f S e) )*"
        ],
    },
]

REGEXP_CFG: list[tuple[str, list[cfg.CFG]]] = [
    (regexp, ds[CFG]) for ds in GRAMMARS_TABLE for regexp in ds[REGEXP]
]
GRAMMARS: list[list[cfg.CFG]] = [ds[CFG] for ds in GRAMMARS_TABLE if len(ds[CFG]) > 1]
GRAMMARS_DIFFERENT: list[cfg.CFG] = [
    ds[CFG][0] for ds in GRAMMARS_TABLE if len(ds[CFG]) >= 1
]
CFG_EBNF: list[tuple[list[cfg.CFG], list[str]]] = sample(
    [(ds[CFG], ds[EBNF]) for ds in GRAMMARS_TABLE], 15
)
REGEXES = sample([regex_str for ds in GRAMMARS_TABLE for regex_str in ds[REGEXP]], 15)
