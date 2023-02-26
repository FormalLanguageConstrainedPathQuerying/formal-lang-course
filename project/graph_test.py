import project.graph_util as gu
import cfpq_data as c_d
import tempfile
import pytest


def test_info():
    graph = c_d.labeled_cycle_graph(1000-7, "???")
    assert gu.get_info(graph) == (993, 993, {"???"})


def test_load():
    graph = gu.load("bzip")
    assert gu.get_info(graph) == (632, 556, {"a", "d"})


def test_build_two_cycles():
    with tempfile.TemporaryFile(mode="w+") as f:
        gu.make_cycles(3, 5, ("a", "d"), f)
        f.seek(0)
        t = f.read()
    assert (
        t == """digraph  {
1;
2;
3;
0;
4;
5;
6;
7;
8;
1 -> 2  [key=0, label=a];
2 -> 3  [key=0, label=a];
3 -> 0  [key=0, label=a];
0 -> 1  [key=0, label=a];
0 -> 4  [key=0, label=d];
4 -> 5  [key=0, label=d];
5 -> 6  [key=0, label=d];
6 -> 7  [key=0, label=d];
7 -> 8  [key=0, label=d];
8 -> 0  [key=0, label=d];
}
"""
    )