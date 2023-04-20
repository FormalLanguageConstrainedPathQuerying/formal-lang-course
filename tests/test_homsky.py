import filecmp
import os.path

import cfpq_data as cfpq
import pytest
from pyformlang.cfg import CFG, Variable, Production, Terminal

from project.homsky import *


def test_info():
    tc = cfpq.labeled_two_cycles_graph(14, 87, labels=("a", "b"))
    i = info(tc)
    assert i.n_c == len(tc.nodes)
    assert i.e_c == len(tc.edges)
    assert set(i.ls) == {"a", "b"}


def test_from_dataset():
    i = from_dataset("bzip")
    assert i.n_c == 632
    assert i.e_c == 556
    assert len(set(i.ls)) == 2


def assertion(c1, c2):
    assert c1.s_s == c2.s_s
    assert c1.ps == c2.ps


def test_homsky():
    s = CFG.from_text("S -> 0 1 1")
    n = to_weak_homsky_form(s)
    assert set(CFG.to_text(n).removesuffix('\n').split('\n')) \
           == {'1#CNF# -> 1', 'C#CNF#1 -> "VAR:1#CNF#" "VAR:1#CNF#"', '0#CNF# -> 0', 'S -> "VAR:0#CNF#" C#CNF#1'}

    s = CFG.from_text("S -> 0 1")
    n = to_weak_homsky_form(s)
    assert set(CFG.to_text(n).removesuffix('\n').split('\n')) \
           == {'1#CNF# -> 1', 'S -> "VAR:0#CNF#" "VAR:1#CNF#"', '0#CNF# -> 0'}

    s = CFG.from_text("S -> 0 0")
    n = to_weak_homsky_form(s)
    assert set(CFG.to_text(n).removesuffix('\n').split('\n')) \
           == {'0#CNF# -> 0', 'S -> "VAR:0#CNF#" "VAR:0#CNF#"'}

    s = CFG.from_text("S -> 1")
    n = to_weak_homsky_form(s)
    assert set(CFG.to_text(n).removesuffix('\n').split('\n')) \
           == {'S -> 1'}

    s = CFG.from_text("S -> epsilon")
    n = to_weak_homsky_form(s)
    assert set(CFG.to_text(n).removesuffix('\n').split('\n')) \
           == {'S -> '}

    s = CFG.from_text("S -> epsilon 0 1")
    n = to_weak_homsky_form(s)
    assert set(CFG.to_text(n).removesuffix('\n').split('\n')) \
           == {'S -> "VAR:0#CNF#" "VAR:1#CNF#"', '0#CNF# -> 0', '1#CNF# -> 1'}

    s = CFG.from_text("S -> A S B | c d\nB -> b\nA -> a")
    n = to_weak_homsky_form(s)
    assert set(CFG.to_text(n).removesuffix('\n').split('\n')) \
           == {'S -> "VAR:c#CNF#" "VAR:d#CNF#"', 'B -> b', 'S -> A C#CNF#1', 'A -> a', 'C#CNF#1 -> S B', 'c#CNF# -> c',
               'd#CNF# -> d'}
