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
7 [label="'true'", shape=box];
6 -> 7;
8 [label="';'", shape=box];
1 -> 8;
9 [label="'<EOF>'", shape=box];
1 -> 9;
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
5 [label="'vertices1'", shape=box];
3 -> 5;
6 [label="'='", shape=box];
3 -> 6;
7 [label=expr];
3 -> 7;
8 [label="'filter'", shape=box];
7 -> 8;
9 [label=lambda];
7 -> 9;
10 [label=args];
9 -> 10;
11 [label=var];
10 -> 11;
12 [label="'v'", shape=box];
11 -> 12;
13 [label="'->'", shape=box];
9 -> 13;
14 [label="'{'", shape=box];
9 -> 14;
15 [label=expr];
9 -> 15;
16 [label=expr];
15 -> 16;
17 [label=var];
16 -> 17;
18 [label="'v'", shape=box];
17 -> 18;
19 [label="'in'", shape=box];
15 -> 19;
20 [label=expr];
15 -> 20;
21 [label=var];
20 -> 21;
22 [label="'s'", shape=box];
21 -> 22;
23 [label="'}'", shape=box];
9 -> 23;
24 [label="'of'", shape=box];
7 -> 24;
25 [label=expr];
7 -> 25;
26 [label="'('", shape=box];
25 -> 26;
27 [label=expr];
25 -> 27;
28 [label="'map'", shape=box];
27 -> 28;
29 [label=lambda];
27 -> 29;
30 [label=args];
29 -> 30;
31 [label="'('", shape=box];
30 -> 31;
32 [label=args];
30 -> 32;
33 [label="'('", shape=box];
32 -> 33;
34 [label=args];
32 -> 34;
35 [label=var];
34 -> 35;
36 [label="'u_g'", shape=box];
35 -> 36;
37 [label="','", shape=box];
32 -> 37;
38 [label=args];
32 -> 38;
39 [label=var];
38 -> 39;
40 [label="'u_q1'", shape=box];
39 -> 40;
41 [label="')'", shape=box];
32 -> 41;
42 [label="','", shape=box];
30 -> 42;
43 [label=args];
30 -> 43;
44 [label=var];
43 -> 44;
45 [label="'l'", shape=box];
44 -> 45;
46 [label="','", shape=box];
30 -> 46;
47 [label=args];
30 -> 47;
48 [label="'('", shape=box];
47 -> 48;
49 [label=args];
47 -> 49;
50 [label=var];
49 -> 50;
51 [label="'v_g'", shape=box];
50 -> 51;
52 [label="','", shape=box];
47 -> 52;
53 [label=args];
47 -> 53;
54 [label=var];
53 -> 54;
55 [label="'v_q1'", shape=box];
54 -> 55;
56 [label="')'", shape=box];
47 -> 56;
57 [label="')'", shape=box];
30 -> 57;
58 [label="'->'", shape=box];
29 -> 58;
59 [label="'{'", shape=box];
29 -> 59;
60 [label=expr];
29 -> 60;
61 [label=var];
60 -> 61;
62 [label="'u_g'", shape=box];
61 -> 62;
63 [label="'}'", shape=box];
29 -> 63;
64 [label="'of'", shape=box];
27 -> 64;
65 [label=expr];
27 -> 65;
66 [label="'('", shape=box];
65 -> 66;
67 [label=expr];
65 -> 67;
68 [label="'get_edges'", shape=box];
67 -> 68;
69 [label=expr];
67 -> 69;
70 [label=var];
69 -> 70;
71 [label="'res1'", shape=box];
70 -> 71;
72 [label="')'", shape=box];
65 -> 72;
73 [label="')'", shape=box];
25 -> 73;
74 [label="';'", shape=box];
1 -> 74;
75 [label="'<EOF>'", shape=box];
1 -> 75;
}
""",
    )
