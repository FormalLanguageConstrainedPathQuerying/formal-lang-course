import pytest
import cfpq_data
import networkx
import project.task1
import random
import pydot
import os

graphs = cfpq_data.dataset.DATASET[0:15]


@pytest.mark.parametrize("graph_name", graphs)
def test_graph_info(graph_name):
    graph_path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(graph_path)

    correct_num_nodes = int(list(str(graph).split(" "))[2])
    correct_num_edges = int(list(str(graph).split(" "))[5])
    correct_labels = set(networkx.get_edge_attributes(graph, "label").values())

    num_nodes, num_edges, labels = project.task1.graph_info(graph_name)

    assert correct_num_nodes == num_nodes
    assert correct_num_edges == num_edges
    assert correct_labels == labels


@pytest.mark.parametrize("i", list(range(10)))
def test_build_and_save_graph_with_two_cicles(i):
    n1 = random.randint(2, 100)
    n2 = random.randint(2, 100)
    file_path = os.path.abspath(f"test_resources/test_build_and_save_graph_with_two_cicles_{i}.dot")
    project.task1.build_and_save_graph_with_two_cicles(n1, n2, file_path)

    readed_graphs = pydot.graph_from_dot_file(file_path)
    readed_graph = networkx.drawing.nx_pydot.from_pydot(readed_graphs[0])

    readed_num_nodes = networkx.number_of_nodes(readed_graph)
    readed_num_edges = networkx.number_of_edges(readed_graph)
    readed_labels = set(networkx.get_edge_attributes(readed_graph, "label").values())

    os.remove(file_path)

    assert readed_num_nodes == n1 + n2 - 1
    assert readed_num_edges == n1 + n2
    assert readed_labels == {"a", "b"}


if __name__ == "__main__":
    test_graph_info()
    test_build_and_save_graph_with_two_cicles()
