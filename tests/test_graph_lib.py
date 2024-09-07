import os
import filecmp
from project import graph_lib

os.chdir("./tests/")


def test_get_get_graph_info_by_name():
    graph_info = graph_lib.get_graph_info_by_name("pizza")
    assert graph_info.nodes_count == 671
    assert graph_info.edges_count == 1980
    assert graph_info.edge_labels == {
        "comment",
        "unionOf",
        "type",
        "domain",
        "allValuesFrom",
        "minCardinality",
        "disjointWith",
        "inverseOf",
        "complementOf",
        "distinctMembers",
        "equivalentClass",
        "versionInfo",
        "intersectionOf",
        "oneOf",
        "subClassOf",
        "range",
        "hasValue",
        "subPropertyOf",
        "label",
        "onProperty",
        "someValuesFrom",
        "rest",
        "first",
    }


def test_create_labeled_two_cycles_graph():
    graph_lib.create_labeled_two_cycles_graph(
        [0, 1, 2, 3, 4, 5], [5, 6, 7], 5, ("fst", "snd"), "test_graph.dot"
    )
    assert filecmp.cmp("test_files/expected_graph.dot", "test_graph.dot", shallow=False)
    os.remove("test_graph.dot")
