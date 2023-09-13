import pytest
from networkx import MultiDiGraph

from project.cfpq.utils import create_labeled_two_cycles_graph


def test_create_labeled_two_cycles_graph():
    expected = MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "a"}),
            (2, 0, {"label": "a"}),
            (0, 3, {"label": "b"}),
            (3, 4, {"label": "b"}),
            (4, 0, {"label": "b"}),
        ]
    )

    actual = create_labeled_two_cycles_graph(2, "a", 2, "b")

    assert expected.nodes == actual.nodes
    assert expected.edges == actual.edges
    assert set(expected.edges.data(data="label")) == set(
        actual.edges.data(data="label")
    )


def test_negative_num_of_nodes_in_labeled_two_cycles_graph():
    with pytest.raises(ValueError):
        create_labeled_two_cycles_graph(0, "a", 4, "b")
    with pytest.raises(ValueError):
        create_labeled_two_cycles_graph(2, "a", -1, "b")
