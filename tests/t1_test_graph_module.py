import os

import project.t1_graph_module as gm


def setup_module(module):
    print("\n\ntest for graph module\n\n")


def teardown_module(module):
    print("\n\nend of test\n\n")


def test_create_and_save_graph():
    gm.create_graph(1, 3, ("1", "2"), "graph.dot")
    assert (
        open("graph.dot", "r").read()
        == """digraph  {
1;
0;
2;
3;
4;
1 -> 0  [key=0, label=1];
0 -> 1  [key=0, label=1];
0 -> 2  [key=0, label=2];
2 -> 3  [key=0, label=2];
3 -> 4  [key=0, label=2];
4 -> 0  [key=0, label=2];
}
"""
    )
    os.remove("graph.dot")


def test_get_info_of_graph():
    assert gm.get_graph_info("atom") == gm.GraphInfo(
        291,
        425,
        {
            "comment",
            "creator",
            "date",
            "description",
            "domain",
            "format",
            "imports",
            "label",
            "language",
            "publisher",
            "range",
            "seeAlso",
            "subClassOf",
            "subPropertyOf",
            "title",
            "type",
            "versionInfo",
        },
    )
