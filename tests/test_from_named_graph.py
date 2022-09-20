from project.graph_utils import GraphData, from_named_graph_to_graph_data


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
    actual_graph_data = from_named_graph_to_graph_data("skos")
    assert actual_graph_data == expected_graph_data
