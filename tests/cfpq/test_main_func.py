from os import path

from project.cfpq.main import load_graph_info_by_name, create_and_save_two_cycles_graph


def test_load_graph_info_by_name():
    actual = load_graph_info_by_name("travel")

    assert 131 == actual["num_of_nodes"]
    assert 277 == actual["num_of_edges"]
    assert {
        "minCardinality",
        "versionInfo",
        "someValuesFrom",
        "equivalentClass",
        "type",
        "range",
        "inverseOf",
        "disjointWith",
        "hasAccommodation",
        "intersectionOf",
        "hasPart",
        "unionOf",
        "comment",
        "oneOf",
        "onProperty",
        "hasValue",
        "subClassOf",
        "rest",
        "differentFrom",
        "complementOf",
        "first",
        "domain",
    } == actual["set_of_labels"]


def test_create_and_save_two_cycles_graph():
    curr_path = path.dirname(path.realpath(__file__))
    expected_path = path.join(curr_path, "expected_graph_main.dot")
    actual_path = path.join(curr_path, "actual_graph_main.dot")

    is_created = create_and_save_two_cycles_graph(
        first_cycle=(5, "abc"),
        second_cycle=(5, "def"),
        path=actual_path,
    )

    assert is_created

    with open(expected_path, "r") as expected_file:
        with open(actual_path, "r") as actual_file:
            assert expected_file.read() == actual_file.read()
