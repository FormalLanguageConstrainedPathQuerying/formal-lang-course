import filecmp
from project.utilities import get_graph_info, generate_two_cycles_graph
import os


def test_get_graph_info():
    info = get_graph_info("skos")

    # from: https: // jetbrains - research.github.io / CFPQ_Data / dataset / index.html
    assert info.n_nodes == 144
    assert info.n_edges == 252
    assert info.edge_labels == {
        "type",
        "label",
        "definition",
        "isDefinedBy",
        "subPropertyOf",
        "comment",
        "scopeNote",
        "inverseOf",
        "range",
        "domain",
        "contributor",
        "disjointWith",
        "creator",
        "example",
        "first",
        "rest",
        "seeAlso",
        "title",
        "description",
        "unionOf",
        "subClassOf",
    }


def test_generate_two_cycles_graph():
    generate_two_cycles_graph(3, 2, ["a", "b"], "tests/test_task1/generated_graph.dot")
    assert filecmp.cmp(
        "tests/test_task1/generated_graph.dot", "tests/test_task1/expected_graph.dot"
    )
    os.remove("tests/test_task1/generated_graph.dot")
