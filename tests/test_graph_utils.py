import pytest
from project.graph_utils import *


def test_correct_name_1():
    result = get_graph_stats("skos")
    expected_result = GraphInfo(
        144,
        252,
        [
            "type",
            "definition",
            "isDefinedBy",
            "label",
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
            "description",
            "seeAlso",
            "subClassOf",
            "title",
            "unionOf",
        ],
    )

    assert [result.nodes, result.edges, result.labels] == [
        expected_result.nodes,
        expected_result.edges,
        expected_result.labels,
    ]


def test_correct_name_2():
    result = get_graph_stats("travel")
    expected_result = GraphInfo(
        131,
        277,
        [
            "type",
            "subClassOf",
            "first",
            "rest",
            "disjointWith",
            "onProperty",
            "domain",
            "range",
            "someValuesFrom",
            "comment",
            "equivalentClass",
            "intersectionOf",
            "differentFrom",
            "hasValue",
            "hasPart",
            "inverseOf",
            "minCardinality",
            "oneOf",
            "complementOf",
            "hasAccommodation",
            "unionOf",
            "versionInfo",
        ],
    )

    assert [result.nodes, result.edges, result.labels] == [
        expected_result.nodes,
        expected_result.edges,
        expected_result.labels,
    ]


def test_incorrect_info():
    result = get_graph_stats("travel")
    expected_result = GraphInfo(
        131,
        287,
        [
            "type",
            "subClassOf",
            "first",
            "rest",
            "disjointWith",
            "onProperty",
            "domain",
            "range",
            "someValuesFrom",
            "comment",
            "equivalentClass",
            "intersectionOf",
            "differentFrom",
            "hasValue",
            "hasPart",
            "inverseOf",
            "minCardinality",
            "oneOf",
            "complementOf",
            "hasAccommodation",
            "unionOf",
            "versionInfo",
        ],
    )

    assert [result.nodes, result.edges, result.labels] != [
        expected_result.nodes,
        expected_result.edges,
        expected_result.labels,
    ]


def test_incorrect_name():
    with pytest.raises(Exception):
        get_graph_stats("this graph doesn't exist")


def test_generate_graph():
    generate_two_cycles_graph(10, 15, "a", "b", "tests/graph.dot", "example_graph")
    assert [row for row in open("tests/graph.dot")] == [
        row for row in open("tests/graph_test.dot")
    ]
