import pytest
import project  # on import will print something from __init__ file
from project.interpreter import *


def setup_module(module):
    print("interpreter test setup module")


def teardown_module(module):
    print("interpreter test teardown module")


def test_interpret_empty():
    res = interpret_string("")
    assert res == ""
    print("test_exec_empty asserted")


def test_interpret_simple():
    assert interpret_string("print 42;") == "42\n"
    assert interpret_string("print {1, 2};") == "[1, 2]\n"
    assert interpret_string("print 1 in {1, 2};") == "True\n"
    assert interpret_string("print 9 in {1...10};") == "True\n"
    assert interpret_string("print 0 in {1, 2};") == "False\n"
    assert interpret_string("let x = 1; print x in {1, 2};") == "True\n"
    assert interpret_string("let x = 42; print x in {1, 2};") == "False\n"


def test_with_loading():
    dir_name = "test_files"
    file12_path = dir_name + "/" + "graphA.txt"
    file21_path = dir_name + "/" + "graphB.txt"

    assert interpret_string(f'let g = load "{file12_path}";') is not None
    assert (
        interpret_string(f'print get_vertices load "{file12_path}";')
        == "['0', '1', '2', '3']\n"
    )

    assert (
        interpret_string(f'print get_edges load "{file12_path}";')
        == "[('0', 'a', '1'), ('0', 'b', '2'), ('1', 'a', '0'), ('2', 'b', '3'), ('3', 'b', '0')]\n"
    )
    assert (
        interpret_string(
            f'let g = load "{file12_path}";'
            f"print get_start g;"
            f'let h = set_start {"{"} 0, 1 {"}"} to g;'
            f"print get_start h;"
        )
        == "['0']\n[0, 1]\n"
    )

    assert (
        interpret_string(
            f'let g = load "{file12_path}";'
            f"print get_final g;"
            f'let h = add_final {"{"} "2" {"}"} to g;'
            f"print get_final h;"
        )
        == "['3']\n['2', '3']\n"
    )

    assert interpret_string(f'print get_labels load "{file12_path}";') == "['a', 'b']\n"

    assert (
        interpret_string(f'print get_reachable load "{file12_path}";')
        == "['0', '1', '2', '3']\n"
    )

    assert (
        interpret_string(
            f'print get_reachable (load "{file21_path}" & load "{file12_path}");'
        )
        == "[]\n"
    )

    assert (
        interpret_string(
            f'print get_reachable (load "{file12_path}" | load "{file21_path}");'
        )
        == "[]\n"
    )

    assert (
        interpret_string(
            f'print map (x1, x2, x3) -> {"{"} x1 {"}"} of (get_edges load "{file12_path}");'
        )
        == "['0', '1', '2', '3']\n"
    )

    assert (
        interpret_string("print filter x -> {x in {0...3}} of {0...100};")
        == "[0, 1, 2]\n"
    )

    assert (
        interpret_string(
            f'print get_vertices (load "{file21_path}" + load "{file12_path}");'
        )
        == "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]\n"
    )

    assert (
        interpret_string(
            f'print get_edges (load "{file12_path}" + load "{file21_path}");'
        )
        == "[(0, 'epsilon', 2), (0, 'epsilon', 20), (2, 'epsilon', 4), (2, 'epsilon', 6), (3, 'epsilon', 1), (4, "
        "'epsilon', 5), (5, 'b', 18), (6, 'epsilon', 8), (6, 'epsilon', 12), (7, 'epsilon', 4), (7, 'epsilon', "
        "6), (8, 'a', 10), (9, 'epsilon', 7), (10, 'epsilon', 11), (11, 'a', 9), (12, 'b', 16), (13, 'epsilon', "
        "7), (14, 'epsilon', 15), (15, 'b', 13), (16, 'epsilon', 17), (17, 'b', 14), (18, 'epsilon', 19), (19, "
        "'b', 3), (20, 'epsilon', 22), (21, 'epsilon', 1), (22, 'epsilon', 23), (23, 'c', 21)]\n"
    )


def test_discard_simple():
    assert interpret_string('print 1 in {"asdfg"};') == "False\n"
    assert interpret_string('let x = 1; print x in {"asdasd"};') == "False\n"
