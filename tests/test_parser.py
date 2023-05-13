import pytest
import project  # on import will print something from __init__ file
from project.parser.parser import satisfy_lang_str


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
    'print get_reachable map (a,) -> { 0 in get_start a } of  *(a & b) >> "abc"; ': False,
    'print get_reachable map (a) -> { 0 of get_start a } of  *(a & b) >> "abc"; ': False,
    'print get_reachable map (a, b, c) -> { 0 in get_start a } of get_edges *(a & b) >> "abc"; ': True,
}


def test_satisfy_lang():
    for k, v in _satisfy_lang_test_cases.items():
        assert satisfy_lang_str(k) == v
