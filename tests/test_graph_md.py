import math
import pytest
import csv
import pathlib
import networkx as nx
from project import t1_graph_utils as t1

DATASET_DIR = pathlib.Path(__file__).parent / "datasets"

GRAPH_SPECS = [
    ("skos", 144, 252),
    ("wc", 332, 269),
    ("travel", 131, 277),
    ("atom", 291, 425),
    ("biomedical", 341, 459),
]


def helper_get_md_directly_from_csv(csv_path):
    nodes_set = set()
    edges_count = 0
    labels = set()

    with open(csv_path, newline="") as f:
        reader = csv.reader(f, delimiter=" ")
        for row in reader:
            source = int(row[0])
            target = int(row[1])
            labels.add(str(row[2]))
            nodes_set.update([source, target])
            edges_count += 1

    expected_nodes = len(nodes_set)
    expected_edges = edges_count

    return [expected_edges, expected_nodes, labels]


def test_empty_graph():
    md = t1.get_graph_md_from_loc_csv(str(DATASET_DIR / "empty_graph.csv"))

    assert md.nodes_num == 0
    assert md.edges_num == 0
    assert md.labels == []


def test_unknown_graph_name():
    with pytest.raises(FileNotFoundError):
        t1.get_graph_md_from_loc_csv("not_existing.csv")


@pytest.mark.parametrize(
    "filename", ["regular_graph_1.csv", "regular_graph_2.csv", "regular_graph_3.csv"]
)
def test_regular_graph_md_compliance(filename):
    filepath = str(DATASET_DIR / filename)
    direct_md = helper_get_md_directly_from_csv(filepath)
    md = t1.get_graph_md_from_loc_csv(str(DATASET_DIR / filename))

    assert md.edges_num == direct_md[0]
    assert md.nodes_num == direct_md[1]
    assert any(md.labels)


@pytest.mark.parametrize(
    "filename", ["regular_graph_1.csv", "regular_graph_2.csv", "regular_graph_3.csv"]
)
def test_label_uniqueness(filename):
    filepath = str(DATASET_DIR / filename)
    direct_md = helper_get_md_directly_from_csv(filepath)
    md = t1.get_graph_md_from_loc_csv(str(DATASET_DIR / filename))

    assert md.edges_num > 0
    assert md.nodes_num > 0
    assert set(md.labels) == direct_md[2]


def test_no_labels_graph():
    filepath = str(DATASET_DIR / "no_labels_graph.csv")
    md = t1.get_graph_md_from_loc_csv(filepath)

    assert md.nodes_num > 0
    assert md.edges_num > 0
    assert all(math.isnan(label) for label in md.labels)


@pytest.mark.parametrize("graph_name, expected_nodes, expected_edges", GRAPH_SPECS)
def test_get_cfpq_graph_by_name(graph_name, expected_nodes, expected_edges):
    graph = t1.get_cfpq_graph_by_name(graph_name)

    assert isinstance(graph, nx.MultiDiGraph)


@pytest.mark.parametrize("graph_name, expected_nodes, expected_edges", GRAPH_SPECS)
def test_get_cfpq_graph_md_by_name(graph_name, expected_nodes, expected_edges):
    md = t1.get_cfpq_graph_md_by_name(graph_name)

    assert md.nodes_num == expected_nodes, f"{graph_name}: nodes mismatch"
    assert md.edges_num == expected_edges, f"{graph_name}: edges mismatch"

    assert all(isinstance(label, str) for label in md.labels)
    assert len(md.labels) == len(set(md.labels)), (
        f"{graph_name}: duplicate labels found"
    )


def test_get_cfpq_graph_by_name_invalid_name():
    with pytest.raises(FileNotFoundError):
        t1.get_cfpq_graph_by_name("non_existing_graph_xyz")
