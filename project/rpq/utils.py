import numpy as np
import networkx as nx
from scipy.sparse import lil_matrix
from project.graph_utils import get_graph_info


def boolean_decomposition(graph: nx.MultiDiGraph) -> dict[lil_matrix]:
    graph_states = list(graph.adj.keys())
    labels = get_graph_info(graph).labels_set
    boolean_decomposition_matrices = {}
    adjacency_matrix = nx.adjacency_matrix(graph).tocoo()
    for label in labels:
        boolean_decomposition_matrices[label] = lil_matrix(
            np.zeros(adjacency_matrix.get_shape())
        )
    for start_vertex, end_vertex in zip(adjacency_matrix.row, adjacency_matrix.col):
        labels_dict = graph[graph_states[start_vertex]][graph_states[end_vertex]]
        for key in labels_dict:
            if "label" in labels_dict[key]:
                boolean_decomposition_matrices[labels_dict[key]["label"]][
                    start_vertex, end_vertex
                ] = 1
    return boolean_decomposition_matrices
