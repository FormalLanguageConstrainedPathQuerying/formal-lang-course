import pytest
from project.grapher import GraphData
import cfpq_data as cfpq


def test_get_graph_data():
    g = GraphData("generations")

    assert g.nodes == 129
    assert g.edges == 273
    assert list(g.edge_labels) == [
        "type",
        "first",
        "rest",
        "onProperty",
        "intersectionOf",
        "equivalentClass",
        "someValuesFrom",
        "hasValue",
        "hasSex",
        "hasChild",
        "hasParent",
        "inverseOf",
        "sameAs",
        "hasSibling",
        "oneOf",
        "range",
        "versionInfo",
    ]
