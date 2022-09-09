from project.utils.graph_utils import get_graph_info

graph_info = get_graph_info("skos")


def test_nodes_number():
    assert graph_info.nodes_num == 144


def test_edges_number():
    assert graph_info.edges_num == 252


def test_labels():
    assert graph_info.labels == {
        "seeAlso",
        "comment",
        "subPropertyOf",
        "rest",
        "type",
        "creator",
        "inverseOf",
        "label",
        "description",
        "unionOf",
        "domain",
        "range",
        "example",
        "scopeNote",
        "contributor",
        "title",
        "subClassOf",
        "definition",
        "first",
        "disjointWith",
        "isDefinedBy",
    }


def test_raise_file_not_found_error():
    try:
        broken = get_graph_info("aaa")
        assert broken.nodes_num == "forty two"
    except FileNotFoundError:
        assert True
