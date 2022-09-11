import filecmp

from project.task1 import GraphData, from_named_graph, write_labeled_two_cycles_graph


def test_from_named_graph():
    expected_graph_data = GraphData(
        144,
        252,
        {
            "isDefinedBy",
            "domain",
            "label",
            "unionOf",
            "comment",
            "definition",
            "subPropertyOf",
            "contributor",
            "creator",
            "subClassOf",
            "range",
            "seeAlso",
            "title",
            "disjointWith",
            "description",
            "type",
            "inverseOf",
            "scopeNote",
            "first",
            "rest",
            "example",
        },
    )
    actual_graph_data = from_named_graph("skos")
    assert actual_graph_data == expected_graph_data


def test_write_labeled_two_cycles_graph():
    write_labeled_two_cycles_graph(
        (3, 3), ("a", "b"), "tests/resources/task1/actual_graph.dot"
    )
    assert filecmp.cmp(
        "tests/resources/task1/actual_graph.dot",
        "tests/resources/task1/expected_graph.dot",
        shallow=False,
    )
