import os
import pytest
import pydot
from project.utils.graph_lib import *


def assert_creation(path):
    first_count_nodes, second_count_nodes, labels = 5, 5, ("some", "none")
    create_two_cycle_graph(first_count_nodes, second_count_nodes, labels, path)
    graph = cfpq_data.labeled_two_cycles_graph(
        first_count_nodes, second_count_nodes, labels=labels
    )
    if not path.endswith(".dot"):
        path = path + ".dot"
    testing_graph = nx.nx_pydot.from_pydot(pydot.graph_from_dot_file(path)[0])
    os.remove(path)
    assert graph.number_of_nodes() == testing_graph.number_of_nodes()
    assert graph.number_of_edges() == testing_graph.number_of_edges()
    assert set(d["label"] for _, _, d in graph.edges(data=True)) == set(
        d["label"] for _, _, d in testing_graph.edges(data=True)
    )


class TestsForCreateTwoCycleGraph:
    def test_with_extension_dot(self):
        assert_creation("test.dot")

    def test_without_extension_dot(self):
        assert_creation("test")


class TestsForGetGraphByName:
    def test_with_existing_graph(self):
        # https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/graphs/data/mm.html#mm
        name = "atom"
        nodes = 291
        edges = 425
        labels = {
            "type",
            "label",
            "subClassOf",
            "comment",
            "domain",
            "range",
            "subPropertyOf",
            "creator",
            "seeAlso",
            "title",
            "description",
            "imports",
            "date",
            "versionInfo",
            "language",
            "publisher",
            "format",
        }
        assert get_graph_by_name(name) == (nodes, edges, labels)

    def test_with_incorrect_graph(self):
        name = "ic heart"
        with pytest.raises(FileNotFoundError):
            get_graph_by_name(name)
