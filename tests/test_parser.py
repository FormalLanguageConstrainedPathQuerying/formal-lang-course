import os
import shutil

import pytest
import project  # on import will print something from __init__ file
from project.parser.parser import satisfy_lang_str, parse_tree_str_to_dot_file


def setup_module(module):
    print("parser setup module")


def teardown_module(module):
    print("parser teardown module")


_satisfy_lang_test_cases = {
    "": True,
    "hello": False,
    "let g = 0;": True,
    "let g = true;": True,
    'let g = load "wine";': True,
    'let g = load "wine"': False,
    "hello world": False,
    "x in {0...10};": False,
    "let x = { } ;": True,
    "print x in { 0, 1 } ; ": True,
    "print x in { 0 ... 1 } ; ": True,
    "/* hsadfgdf */": True,
    "let a = 0;"
    "print 1;"
    "print a;"
    'print get_start load "gr.txt"; '
    "/* a */": True,
    'let a = load "a"; let b = load "b"; '
    "print a & b | a + b;"
    'print *(a & b) >> "abc"; ': True,
    "print print 0": False,
    'print a in b | load "a";': True,
    "print filter (a) -> { false } of a; ": True,
    'print filter (a) -> { 0 in (get_start a) } of load "abc"; ': True,
    'print map (a) -> { 0 in get_start a } of  *(a & b) >> "abc"; ': True,
    'print get_reachable map (a) -> { 0 in get_start a } of  *(a & b) >> "abc"; ': True,
    'print get_reachable map a -> { 0 in get_start a } of  *(a & b) >> "abc"; ': True,
    'print get_reachable map (a,) -> { 0 in get_start a } of  *(a & b) >> "abc"; ': False,
    'print get_reachable map (a) -> { 0 of get_start a } of  *(a & b) >> "abc"; ': False,
    'print get_reachable map (a, b, c) -> { 0 in get_start a } of get_edges *(a & b) >> "abc"; ': True,
}


def test_satisfy_lang():
    for k, v in _satisfy_lang_test_cases.items():
        assert satisfy_lang_str(k) == v


def _assert_parse_tree_dot(text: str, expected_graph: str):
    dir_name = f"test_parse_tree_to_dot_file{len(text)}-{text[0:10]}"
    file_name = f"/1.dot"
    try:
        os.mkdir(dir_name)
        parse_tree_str_to_dot_file(text, dir_name + file_name)
        with open(dir_name + file_name) as file:
            file_lines = "".join(file.readlines())
            assert file_lines == expected_graph
    except Exception as e:
        assert e is None
    finally:
        shutil.rmtree(dir_name)


def test_1_parse_tree_to_dot_file():
    _assert_parse_tree_dot(
        "",
        """\
strict digraph parse_tree {
1 [label=prog];
0 -> 1;
2 [label="'<EOF>'", shape=box];
1 -> 2;
}
""",
    )


def test_2_parse_tree_to_dot_file():
    _assert_parse_tree_dot(
        "print true;",
        """\
strict digraph parse_tree {
1 [label=prog];
0 -> 1;
2 [label=stmt];
1 -> 2;
3 [label=print];
2 -> 3;
4 [label="'print'", shape=box];
3 -> 4;
5 [label=expr];
3 -> 5;
6 [label=val];
5 -> 6;
7 [label=valBool];
6 -> 7;
8 [label="'true'", shape=box];
7 -> 8;
9 [label="';'", shape=box];
1 -> 9;
10 [label="'<EOF>'", shape=box];
1 -> 10;
}
""",
    )


def test_3_parse_tree_to_dot_file():
    _assert_parse_tree_dot(
        "let vertices1 = filter v -> {v in s} of"
        " (map ((u_g,u_q1),l,(v_g,v_q1)) -> {u_g} of (get_edges res1));",
        """\
strict digraph parse_tree {
1 [label=prog];
0 -> 1;
2 [label=stmt];
1 -> 2;
3 [label=bind];
2 -> 3;
4 [label="'let'", shape=box];
3 -> 4;
5 [label=var];
3 -> 5;
6 [label="'vertices1'", shape=box];
5 -> 6;
7 [label="'='", shape=box];
3 -> 7;
8 [label=expr];
3 -> 8;
9 [label="'filter'", shape=box];
8 -> 9;
10 [label=lambda];
8 -> 10;
11 [label=args];
10 -> 11;
12 [label=var];
11 -> 12;
13 [label="'v'", shape=box];
12 -> 13;
14 [label="'->'", shape=box];
10 -> 14;
15 [label="'{'", shape=box];
10 -> 15;
16 [label=expr];
10 -> 16;
17 [label=expr];
16 -> 17;
18 [label=var];
17 -> 18;
19 [label="'v'", shape=box];
18 -> 19;
20 [label="'in'", shape=box];
16 -> 20;
21 [label=expr];
16 -> 21;
22 [label=var];
21 -> 22;
23 [label="'s'", shape=box];
22 -> 23;
24 [label="'}'", shape=box];
10 -> 24;
25 [label="'of'", shape=box];
8 -> 25;
26 [label=expr];
8 -> 26;
27 [label="'('", shape=box];
26 -> 27;
28 [label=expr];
26 -> 28;
29 [label="'map'", shape=box];
28 -> 29;
30 [label=lambda];
28 -> 30;
31 [label=args];
30 -> 31;
32 [label="'('", shape=box];
31 -> 32;
33 [label=args];
31 -> 33;
34 [label="'('", shape=box];
33 -> 34;
35 [label=args];
33 -> 35;
36 [label=var];
35 -> 36;
37 [label="'u_g'", shape=box];
36 -> 37;
38 [label="','", shape=box];
33 -> 38;
39 [label=args];
33 -> 39;
40 [label=var];
39 -> 40;
41 [label="'u_q1'", shape=box];
40 -> 41;
42 [label="')'", shape=box];
33 -> 42;
43 [label="','", shape=box];
31 -> 43;
44 [label=args];
31 -> 44;
45 [label=var];
44 -> 45;
46 [label="'l'", shape=box];
45 -> 46;
47 [label="','", shape=box];
31 -> 47;
48 [label=args];
31 -> 48;
49 [label="'('", shape=box];
48 -> 49;
50 [label=args];
48 -> 50;
51 [label=var];
50 -> 51;
52 [label="'v_g'", shape=box];
51 -> 52;
53 [label="','", shape=box];
48 -> 53;
54 [label=args];
48 -> 54;
55 [label=var];
54 -> 55;
56 [label="'v_q1'", shape=box];
55 -> 56;
57 [label="')'", shape=box];
48 -> 57;
58 [label="')'", shape=box];
31 -> 58;
59 [label="'->'", shape=box];
30 -> 59;
60 [label="'{'", shape=box];
30 -> 60;
61 [label=expr];
30 -> 61;
62 [label=var];
61 -> 62;
63 [label="'u_g'", shape=box];
62 -> 63;
64 [label="'}'", shape=box];
30 -> 64;
65 [label="'of'", shape=box];
28 -> 65;
66 [label=expr];
28 -> 66;
67 [label="'('", shape=box];
66 -> 67;
68 [label=expr];
66 -> 68;
69 [label="'get_edges'", shape=box];
68 -> 69;
70 [label=expr];
68 -> 70;
71 [label=var];
70 -> 71;
72 [label="'res1'", shape=box];
71 -> 72;
73 [label="')'", shape=box];
66 -> 73;
74 [label="')'", shape=box];
26 -> 74;
75 [label="';'", shape=box];
1 -> 75;
76 [label="'<EOF>'", shape=box];
1 -> 76;
}
""",
    )
