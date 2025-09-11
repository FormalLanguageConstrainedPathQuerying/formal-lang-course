import cfpq_data
import networkx as nx


def graph_info(graph_name: str) -> tuple[int, int, set[str]]:
    """
    Возвращает информацию о графе:
    - количество вершин
    - количество рёбер
    - множество меток на рёбрах
    """
    graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_name))
    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        set(nx.get_edge_attributes(graph, "label").values()),
    )


def two_cycles_graph(n: int, m: int, labels: tuple[str, str], path: str) -> None:
    """
    Строит граф из двух циклов с длинами n и m и метками labels,
    сохраняет в файл path в формате DOT.
    """
    if len(labels) != 2:
        raise ValueError("Нужно передать 2 метки для двух циклов.")

    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    nx.drawing.nx_pydot.to_pydot(graph).write_raw(path)
