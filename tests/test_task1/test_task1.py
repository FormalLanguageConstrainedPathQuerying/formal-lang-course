import filecmp
import networkx as nx
from pytest import raises

from project.graph_utils import (
    get_graph_info,
    get_graph_info_by_name,
    generate_two_cycles_graph,
)


def test_get_graph_info_null():
    info = get_graph_info(nx.null_graph())

    assert info.number_of_nodes == 0
    assert info.number_of_edges == 0
    assert info.edge_labels == set()


def test_get_graph_info_trivial():
    info = get_graph_info(nx.trivial_graph())

    assert info.number_of_nodes == 1
    assert info.number_of_edges == 0
    assert info.edge_labels == set()


def test_get_graph_info_loop():
    info = get_graph_info(nx.Graph([(0, 0, {"label": "a"})]))

    assert info.number_of_nodes == 1
    assert info.number_of_edges == 1
    assert info.edge_labels == {"a"}


def test_get_graph_info_bad_name():
    with raises(ValueError):
        get_graph_info_by_name("bad_name")


# функция cfpq_data.download сломана

# def test_get_graph_info_skos():
#     info = get_graph_info_by_name("skos")
#
#     assert info.number_of_nodes == 144
#     assert info.number_of_edges == 252
#     assert info.edge_labels == {
#         "type",
#         "label",
#         "definition",
#         "isDefinedBy",
#         "subPropertyOf",
#         "comment",
#         "scopeNote",
#         "inverseOf",
#         "range",
#         "domain",
#         "contributor",
#         "disjointWith",
#         "creator",
#         "example",
#         "first",
#         "rest",
#         "seeAlso",
#         "title",
#         "description",
#         "unionOf",
#         "subClassOf",
#     }


def test_generate_two_cycles_graph_0_0(tmp_path):
    with raises(ValueError):
        generate_two_cycles_graph(0, 0, "./generated_graph.dot")


def test_generate_two_cycles_graph_0_1(tmp_path):
    with raises(ValueError):
        generate_two_cycles_graph(0, 1, "./generated_graph.dot")


def test_generate_two_cycles_graph_1_1(tmp_path):
    expected_content = """
    digraph  {
    1;
    0;
    2;
    1 -> 0  [key=0, label=a];
    0 -> 1  [key=0, label=a];
    0 -> 2  [key=0, label=b];
    2 -> 0  [key=0, label=b];
    }
    """
    path_of_expected_graph = tmp_path / "expected_graph.dot"
    path_of_generated_graph = tmp_path / "expected_graph.dot"

    with open(path_of_expected_graph, "w") as f:
        f.write(expected_content)
    generate_two_cycles_graph(1, 1, path_of_generated_graph)
    assert filecmp.cmp(path_of_generated_graph, path_of_expected_graph)


def test_generate_two_cycles_graph(tmp_path):
    expected_content = """
    digraph  {
    1;
    2;
    3;
    0;
    4;
    5;
    1 -> 2  [key=0, label=a];
    2 -> 3  [key=0, label=a];
    3 -> 0  [key=0, label=a];
    0 -> 1  [key=0, label=a];
    0 -> 4  [key=0, label=b];
    4 -> 5  [key=0, label=b];
    5 -> 0  [key=0, label=b];
    }
    """
    path_of_expected_graph = tmp_path / "expected_graph.dot"
    path_of_generated_graph = tmp_path / "expected_graph.dot"

    with open(path_of_expected_graph, "w") as f:
        f.write(expected_content)
    generate_two_cycles_graph(3, 2, path_of_generated_graph)
    assert filecmp.cmp(path_of_generated_graph, path_of_expected_graph)
