import pathlib
import pytest
import networkx as nx
from project import t1_graph_utils as t1

TMP_DATASET_DIR = pathlib.Path(__file__).parent / "datasets/tmp"


@pytest.fixture
def tmp_dataset_dir():
    try:
        TMP_DATASET_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        print("Creation of the directory %s failed" % TMP_DATASET_DIR)
    else:
        print("Successfully created the directory %s " % TMP_DATASET_DIR)

    yield TMP_DATASET_DIR
    for file in TMP_DATASET_DIR.iterdir():
        if file.is_file():
            file.unlink()


def test_save_nx_graph_to_dot_creates_file(tmp_dataset_dir):
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="b")

    filename = TMP_DATASET_DIR / "graph.dot"
    t1.save_nx_graph_to_dot(graph, str(filename))

    assert filename.exists()
    content = filename.read_text()
    assert "digraph" in content or "graph" in content

    loaded_graph = t1.read_graph_from_dot(filename)
    assert loaded_graph.number_of_nodes() == 3
    assert loaded_graph.number_of_edges() == 2
    edge_labels = [d.get("label") for _, _, d in loaded_graph.edges(data=True)]
    assert "a" in edge_labels
    assert "b" in edge_labels


def test_empty_graph_dot(tmp_dataset_dir):
    graph = nx.MultiDiGraph()
    filename = TMP_DATASET_DIR / "empty_graph.dot"
    t1.save_nx_graph_to_dot(graph, str(filename))

    assert filename.exists()

    loaded_graph = t1.read_graph_from_dot(filename)
    assert loaded_graph.number_of_nodes() == 0
    assert loaded_graph.number_of_edges() == 0


def test_single_cycle_graph(tmp_dataset_dir):
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 0, label="a")
    filename = TMP_DATASET_DIR / "single_cycle.dot"
    t1.save_nx_graph_to_dot(graph, str(filename))

    loaded_graph = t1.read_graph_from_dot(filename)
    assert loaded_graph.number_of_nodes() == 2
    assert loaded_graph.number_of_edges() == 2
    labels = [d.get("label") for _, _, d in loaded_graph.edges(data=True)]
    assert labels.count("a") == 2
