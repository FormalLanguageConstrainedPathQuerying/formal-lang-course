import random
import cfpq_data
import copy
from networkx import MultiDiGraph
import itertools
import networkx as nx
from constants import *


def generate_rnd_graph(
    min_size: int, max_size: int, labels: list[str]
) -> nx.MultiDiGraph:
    n_of_nodes = random.randint(min_size, max_size)
    return cfpq_data.graphs.labeled_scale_free_graph(n_of_nodes, labels=labels)


def generate_rnd_dense_graph(
    min_size: int, max_size: int, labels: list[str]
) -> MultiDiGraph:
    n_of_nodes = random.randint(min_size, max_size)
    return cfpq_data.graphs.labeled_binomial_graph(n=n_of_nodes, p=0.4, labels=labels)


def generate_rnd_start_and_final(graph: nx.MultiDiGraph) -> tuple[set[int], set[int]]:
    start_nodes = set(
        random.choices(
            list(graph.nodes().keys()), k=random.randint(1, len(graph.nodes))
        )
    )
    final_nodes = set(
        random.choices(
            list(graph.nodes().keys()), k=random.randint(1, len(graph.nodes))
        )
    )

    for node, data in graph.nodes(data=True):
        if node in start_nodes:
            data[IS_START] = True
        if node in final_nodes:
            data[IS_FINAL] = True
    return start_nodes, final_nodes


def rpq_dict_to_set(rpq: dict[int, set[int]]) -> set[tuple[int, int]]:
    rpq_set = set()
    for node_from, nodes_to in rpq.items():
        for node_to in nodes_to:
            rpq_set.add((node_from, node_to))
    return rpq_set


class GraphWordsHelper:
    graph = None
    final_nodes = None
    transitive_closure = None
    start_nodes = None

    def __init__(self, graph: MultiDiGraph):
        self.graph = graph.copy()
        self.final_nodes = {
            node for node, data in self.graph.nodes(data=IS_FINAL) if data
        }
        self.start_nodes = {
            node for node, data in self.graph.nodes(data=IS_START) if data
        }
        self.transitive_closure: nx.MultiDiGraph = nx.transitive_closure(
            copy.deepcopy(self.graph), reflexive=False
        )

    def is_reachable(self, source, target):
        return target in self.transitive_closure[source].keys()

    def _exists_any_final_path(self, node):
        return any(
            self.is_reachable(node, final_node) for final_node in self.final_nodes
        )

    def _take_a_step(self, node):
        for node_to, edge_dict in dict(self.graph[node]).items():
            for edge_data in edge_dict.values():
                yield node_to, edge_data[LABEL]

    def _is_final_node(self, node):
        return node in self.final_nodes

    def generate_words_by_node(self, node):
        queue = [(node, [])]
        while len(queue) != 0:
            (n, word) = queue.pop(0)
            for node_to, label in self._take_a_step(n):
                tmp = word.copy()
                tmp.append(label)
                if self._is_final_node(node_to):
                    yield tmp.copy()
                if self._exists_any_final_path(node_to):
                    queue.append((node_to, tmp.copy()))

    def take_n_words_by_node(self, node, n):
        if self._exists_any_final_path(node):
            return list(itertools.islice(self.generate_words_by_node(node), 0, n))
        return []

    def get_words_with_limiter(self, limiter: int) -> list[str]:
        result = list()
        for start in self.start_nodes:
            result.extend(self.take_n_words_by_node(start, limiter))
            if start in self.final_nodes:
                result.append([])
        return result
