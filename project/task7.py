from collections import defaultdict
import networkx as nx
import numpy as np
from pyformlang.cfg import CFG, Terminal, Variable
from scipy.sparse import csr_matrix
from project.task6 import cfg_to_weak_normal_form


class CFPQMatrix:
    def __init__(self, cfg, graph, matrix_type=csr_matrix):
        self.cfg = cfg
        self.graph = graph
        self.nodes_amount = graph.number_of_nodes()
        self.matrix_type = matrix_type
        self.node_to_index = {node: idx for idx, node in enumerate(graph.nodes())}
        self.index_to_node = list(graph.nodes())

        self.var_matrices = defaultdict(
            lambda: self.matrix_type((self.nodes_amount, self.nodes_amount), dtype=bool)
        )
        self.__initialize_matrices()

    def __initialize_matrices(self):
        for u, v, data in self.graph.edges(data=True):
            label = data.get("label")
            if label is None:
                continue
            for prod in self.cfg.productions:
                if (
                    len(prod.body) == 1
                    and isinstance(prod.body[0], Terminal)
                    and prod.body[0].value == label
                ):
                    self.var_matrices[prod.head][
                        self.node_to_index[u], self.node_to_index[v]
                    ] = True

        nullable_vars = self.cfg.get_nullable_symbols()
        for node in self.graph.nodes:
            idx = self.node_to_index[node]
            for var in nullable_vars:
                self.var_matrices[Variable(var.value)][idx, idx] = True

        self.__apply_hellings()

    def __apply_hellings(self):
        change = True
        while change:
            change = False
            for prod in self.cfg.productions:
                if len(prod.body) == 2:
                    B, C = Variable(prod.body[0].value), Variable(prod.body[1].value)
                    head = prod.head
                    if B in self.var_matrices and C in self.var_matrices:
                        product_matrix = self.var_matrices[B] @ self.var_matrices[C]
                        added_indices = np.transpose(product_matrix.nonzero())
                        for u, v in added_indices:
                            if not self.var_matrices[head][u, v]:
                                self.var_matrices[head][u, v] = True
                                change = True

    def get_reachable_pairs(self, start_nodes, final_nodes):
        result = set()
        start_symbol = self.cfg.start_symbol
        if start_symbol in self.var_matrices:
            for u, v in zip(*self.var_matrices[start_symbol].nonzero()):
                node_u, node_v = self.index_to_node[u], self.index_to_node[v]
                if (not start_nodes or node_u in start_nodes) and (
                    not final_nodes or node_v in final_nodes
                ):
                    result.add((node_u, node_v))
        return result


def matrix_based_cfpq(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    matrix_type=csr_matrix,
) -> set[tuple[int, int]]:
    weak_normal_form = cfg_to_weak_normal_form(cfg)
    result = CFPQMatrix(weak_normal_form, graph, matrix_type).get_reachable_pairs(
        start_nodes, final_nodes
    )

    return result
