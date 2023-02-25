from project.task01.graph import *


def test_graph_info():
    graph_name = "generations"
    V, E, L = graph_info(graph_name)
    assert 1687 == V
    assert 1453 == E
    assert ["d", "a"] == L


def test_create_graph():
    filename = "test_create_graph.dot"
    expected = (
        "digraph  { 1; 2; 0; 3; 4; 5; 6; 1 -> 2  [key=0, label=a]; 2 -> 0  [key=0, label=a]; 0 -> 1  [key=0, "
        "label=a]; 0 -> 3  [key=0, label=c]; 3 -> 4  [key=0, label=c]; 4 -> 5  [key=0, label=c]; 5 -> 6  ["
        "key=0, label=c]; 6 -> 0  [key=0, label=c]; } "
    )
    create_graph(2, 4, ["a", "c"], filename)
    with open(filename, "r") as f:
        assert expected == f.read().replace("\n", " ")
