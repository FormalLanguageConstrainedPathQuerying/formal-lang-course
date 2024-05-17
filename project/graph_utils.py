import cfpq_data as cd
from typing import *
import networkx


def get_nvertex_nedges_numerate_marks(graph_name: str) -> tuple[int, int, List]:
    """
    Получить количество вершин, количество ребер, список меток по названию графа
    """
    graph_path = cd.download(graph_name)
    graph = cd.graph_from_csv(graph_path)

    list_of_marks = []
    for edge in graph.edges:
        list_of_marks.append((edge, graph.edges[edge]["label"]))
    return (graph.number_of_nodes(), graph.number_of_edges(), list_of_marks)


def create_labeled_two_cycles_graph(
    filename: str, n: int, m: int, labels: Tuple[str, str]
) -> bool:
    """
    Получить граф с двумя циклами соедененными одним узлом. С помеченными ребрами (один цикл labels[0])
    , в то же время второй цикл labels[1]
    """
    graph = cd.labeled_two_cycles_graph(n, m, labels=labels)
    graph_pydot = networkx.drawing.nx_pydot.to_pydot(graph)
    return graph_pydot.write(filename)
