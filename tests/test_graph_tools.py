from pathlib import Path
from project.graph_tools import (
    GraphData,
    create_and_save_two_cycle_graph,
)
import pytest
from tempfile import NamedTemporaryFile
import networkx as nx


@pytest.mark.parametrize(
    "name, expected_graph_data",
    [
        (
            "wc",
            GraphData(
                nodes_count=332,
                edges_count=269,
                labels={"d", "a"},
            ),
        ),
        (
            "enzyme",
            GraphData(
                nodes_count=48815,
                edges_count=86543,
                labels={
                    "activity",
                    "altLabel",
                    "broaderTransitive",
                    "cofactorLabel",
                    "comment",
                    "imports",
                    "label",
                    "narrowerTransitive",
                    "obsolete",
                    "prefLabel",
                    "replacedBy",
                    "replaces",
                    "subClassOf",
                    "type",
                },
            ),
        ),
    ],
)
def test_get_graph_data_by_name(name: str, expected_graph_data: GraphData):
    graph_data = GraphData.get_graph_data_by_name(name)
    assert graph_data == expected_graph_data


def test_get_graph_data_by_name_fail():
    with pytest.raises(FileNotFoundError):
        GraphData.get_graph_data_by_name("Invalid graph name")


EXPECTED_PATH = Path(__file__).parent / "expected"

test_graph_data = [
    (42, 42, ("Bob", "Alice"), EXPECTED_PATH / "first_graph.dot"),
    (17, 88, ("888", "1700"), EXPECTED_PATH / "second_graph.dot"),
]


@pytest.mark.parametrize("n1,n2,labels,expected_path", test_graph_data)
def test_build_save_2cycles_graph(
    n1: int,
    n2: int,
    labels: tuple[str, str],
    expected_path: Path,
):
    with NamedTemporaryFile() as tmp:
        create_and_save_two_cycle_graph(n1, n2, labels, Path(tmp.name))
        actual: nx.MultiDiGraph = nx.nx_pydot.read_dot(tmp.name)

    expected: nx.MultiDiGraph = nx.nx_pydot.read_dot(expected_path)
    assert nx.utils.graphs_equal(actual, expected)
