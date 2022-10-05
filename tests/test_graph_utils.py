import filecmp

import pytest

from project.__init__ import *
import networkx as nx


@pytest.mark.parametrize(
    "two_cycles_graph", [[40, 40, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_comparison_two_cycles_graph(two_cycles_graph):
    graph = create_two_cycles_graph(40, 40, ("a", "b"))
    em = nx.algorithms.isomorphism.categorical_multiedge_match("label", None)
    assert nx.is_isomorphic(graph, two_cycles_graph, edge_match=em)


@pytest.mark.parametrize(
    "two_cycles_graph", [[40, 40, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_save_graph_in_dot(two_cycles_graph):
    save_in_dot(two_cycles_graph)
    assert filecmp.cmp(
        str(shared.ROOT) + os.sep + "output" + os.sep + "graph.dot",
        str(shared.ROOT) + os.sep + "output" + os.sep + "expected_graph.dot",
    )


@pytest.mark.parametrize(
    "two_cycles_graph", [[3, 3, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_get_graph_info_by_graph(two_cycles_graph):
    info_by_graph = get_info_by_graph(two_cycles_graph)
    assert info_by_graph.number_of_nodes == 7
    assert info_by_graph.number_of_edges == 8
    assert info_by_graph.labels == {"a", "b"}


# def test_get_graph_info_by_name():
#     info_by_name = get_info_by_name("univ")
#     assert info_by_name.number_of_nodes == 179
#     assert info_by_name.number_of_edges == 293
#     assert info_by_name.labels == {
#         "someValuesFrom",
#         "first",
#         "intersectionOf",
#         "subClassOf",
#         "range",
#         "rest",
#         "comment",
#         "type",
#         "versionInfo",
#         "subPropertyOf",
#         "label",
#         "domain",
#         "onProperty",
#         "inverseOf",
#     }
