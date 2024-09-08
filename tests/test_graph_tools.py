from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from networkx import MultiDiGraph, nx_pydot
from networkx.utils import graphs_equal

from project.graph_tools import (
    GraphMetadata,
    build_save_2cycles_graph,
    get_graph_metadata,
)

EXPECTED_PATH = Path(__file__).parent / "expected"


graph_meta_testdata = [
    ("wc", GraphMetadata(node_count=332, edge_count=269, edge_labels={"d", "a"})),
    (
        "pathways",
        GraphMetadata(
            node_count=6238,
            edge_count=12363,
            edge_labels={"subClassOf", "narrower", "imports", "type", "label"},
        ),
    ),
]


@pytest.mark.parametrize("graph_name,expected", graph_meta_testdata)
def test_get_graph_metadata(graph_name: str, expected: GraphMetadata):
    actual = get_graph_metadata(graph_name)
    assert actual == expected


two_cycles_testdata = [
    (10, "fst", 20, "snd", EXPECTED_PATH / "two_cycles1.dot"),
    (1, "c1", 41, "c2", EXPECTED_PATH / "two_cycles2.dot"),
]


@pytest.mark.parametrize(
    "nodes1,labels1,nodes2,labels2,expected_path", two_cycles_testdata
)
def test_build_save_2cycles_graph(
    nodes1: int,
    labels1: str,
    nodes2: int,
    labels2: str,
    expected_path: Path,
):
    with NamedTemporaryFile() as tmp:
        build_save_2cycles_graph(nodes1, labels1, nodes2, labels2, tmp.name)
        actual: MultiDiGraph = nx_pydot.read_dot(tmp.name)

    expected: MultiDiGraph = nx_pydot.read_dot(expected_path)

    assert graphs_equal(actual, expected)
