import filecmp
import os
import networkx
from networkx import nx_pydot

from project.graph_manager import GraphManager


def test_get_info():
    actual = GraphManager.get_info("generations")
    expected = (
        129,
        273,
        [
            "rest",
            "first",
            "onProperty",
            "type",
            "hasValue",
            "someValuesFrom",
            "equivalentClass",
            "intersectionOf",
            "inverseOf",
            "range",
            "hasSibling",
            "sameAs",
            "hasParent",
            "hasSex",
            "hasChild",
            "versionInfo",
            "oneOf",
        ],
    )

    assert actual == expected


def test_write_two_cycle_labeled_graph_to_dot():
    path = os.path.dirname(os.path.abspath(__file__)) + "/res"
    actual = path + "/actual.dot"
    expected = path + "/expected.dot"

    GraphManager.create_two_cycle_labeled_graph((2, 3), ("a", "b"), actual)
    filecmp.cmp(actual, expected)
    os.remove(actual)


def test_create_two_cycle_labeled_graph():
    path = os.path.dirname(os.path.abspath(__file__)) + "/res/expected.dot"
    expected = nx_pydot.read_dot(path)

    sizes = (2, 3)
    labels = ("a", "b")
    actual = GraphManager._GraphManager__create_two_cycle_labeled_graph(sizes, labels)

    networkx.is_isomorphic(
        actual,
        expected,
        node_match=expected.nodes,
        edge_match=expected.edges(data=True),
    )
