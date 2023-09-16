import filecmp
import os
from cfpq_data import labeled_two_cycles_graph
from project.graph_utility.graph_utility import *
from pytest import raises


def test_load_graph():
    # Graph from https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/reference/graphs/generated/cfpq_data.graphs.readwrite.csv.html#module-cfpq_data.graphs.readwrite.csv
    graph = load_graph("generations")
    assert graph.number_of_edges() == 273
    assert graph.number_of_nodes() == 129
    assert set(label for _, _, label in graph.edges.data(data="label")) == {
        "hasSibling",
        "someValuesFrom",
        "versionInfo",
        "sameAs",
        "oneOf",
        "range",
        "first",
        "type",
        "hasValue",
        "equivalentClass",
        "intersectionOf",
        "inverseOf",
        "hasParent",
        "onProperty",
        "rest",
        "hasChild",
        "hasSex",
    }


def test_load_undefined_graph():
    with raises(Exception):
        load_graph("undefined")


def test_get_graph_info():
    graph_info = get_graph_info("generations")
    assert graph_info[0] == 273
    assert graph_info[1] == 129
    assert graph_info[2] == {
        "hasSibling",
        "someValuesFrom",
        "versionInfo",
        "sameAs",
        "oneOf",
        "range",
        "first",
        "type",
        "hasValue",
        "equivalentClass",
        "intersectionOf",
        "inverseOf",
        "hasParent",
        "onProperty",
        "rest",
        "hasChild",
        "hasSex",
    }


def test_create_graph_of_two_cycles():
    n = 5
    m = 3
    labels = ("a", "b")
    actual_graph = create_graph_of_two_cycles(
        first_cycle_nodes=n, second_cycle_nodes=m, labels=labels
    )
    expected_graph = labeled_two_cycles_graph(n=n, m=m, labels=labels)

    assert expected_graph.nodes == actual_graph.nodes
    assert list(expected_graph.edges.data(data="label")) == list(
        actual_graph.edges.data(data="label")
    )


def test_save_graph_as_dot():
    n = 3
    m = 3
    labels = ("a", "b")
    current_dir_path = path.dirname(path.realpath(__file__))
    graph = labeled_two_cycles_graph(n=n, m=m, labels=labels)
    save_graph_as_dot(
        graph=graph,
        output_name="test_result",
        output_path=path.join(current_dir_path, "result"),
    )

    assert filecmp.cmp(
        path.join(current_dir_path, "result", "test_result.dot"),
        path.join(current_dir_path, "result", "sample.dot"),
        shallow=False,
    )

    os.remove(path.join(current_dir_path, "result", "test_result.dot"))
