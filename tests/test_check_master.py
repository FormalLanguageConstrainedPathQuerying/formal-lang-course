import pytest
import pydot
from project.check_master import *


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_grammar_check():
    assert is_valid("let a = 1;")
    assert is_valid("$ a;")
    assert is_valid("let a = (1);")
    assert is_valid("let a = (1);")
    assert is_valid("let a = a~;")
    assert is_valid("let a = a := start b;")
    assert is_valid("let a = a += final c;")
    assert is_valid("let a = a ?? reachable;")
    assert is_valid("let a = b -> {c} --> d;")
    assert is_valid("let a = b -> {c} ?-> d;")
    assert is_valid("let a = # P'path';")
    assert is_valid("let a = b + c;")


def test_dot():
    r = convert_to_dot("let a = 1 <= 'c';let a = 1 && 'c';let a = b + 'c';")
    assert r.to_string() != ""