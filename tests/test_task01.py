import project.task01 as mod
from os import path
import tempfile
import filecmp

dirpath = path.dirname(path.realpath(__file__))


def test_get_graph_props_by_name():

    with open(f"{dirpath}/test_data/task01/edges_data", "r") as f:
        edges_data = f.readline().strip()

    nodes_count = 144
    edges_count = 252

    graph_props: mod.GraphProps = mod.get_graph_props_by_name(name="skos")
    assert nodes_count == graph_props.nodes_count
    assert edges_count == graph_props.edges_count
    assert edges_data == str(graph_props.edges_data).strip()


def test_two_cycle_graph_to_dot():
    with tempfile.NamedTemporaryFile() as tmp:
        path = tmp.name
    n = 5
    m = 7
    mod.two_cycle_graph_to_dot(path=tmp.name, n=n, m=m)
    assert filecmp.cmp(f"{dirpath}/test_data/task01/test.dot", path)
