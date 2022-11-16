from cfpq_data import *
from networkx import MultiDiGraph, nx_pydot
from pyformlang.cfg import Variable, CFG
from project.cfg_manager import CFGManager


class GraphManager:
    @staticmethod
    def get_info(name: str) -> tuple[int, int, list[str]]:
        graph = GraphManager.__get_graph(name)
        labels = GraphManager.__get_labels(graph)
        return graph.number_of_nodes(), graph.number_of_edges(), labels

    @staticmethod
    def create_two_cycle_labeled_graph(
        sizes: tuple[int, int], labels: tuple[str, str], path: str
    ) -> None:
        graph = GraphManager.__create_two_cycle_labeled_graph(sizes, labels)
        nx_pydot.write_dot(graph, path)

    @staticmethod
    def execute_cfpq(
        cfg: CFG,
        graph: MultiDiGraph,
        start_symbol: Variable = Variable("S"),
        start_nodes: set = None,
        final_nodes: set = None,
    ) -> set:
        start_nodes = graph.nodes if start_nodes is None else start_nodes
        final_nodes = graph.nodes if final_nodes is None else final_nodes

        return {
            (u, v)
            for (N, u, v) in GraphManager.__run_hellings(cfg, graph)
            if (N == start_symbol) and (u in start_nodes) and (v in final_nodes)
        }

    @staticmethod
    def __get_graph(name: str) -> MultiDiGraph:
        path = cfpq_data.download(name)
        return cfpq_data.graph_from_csv(path)

    @staticmethod
    def __get_labels(graph: MultiDiGraph) -> list[str]:
        labels = []
        [
            labels.append(edge[2]["label"])
            for edge in graph.edges.data()
            if (edge[2]["label"]) not in labels
        ]
        return labels

    @staticmethod
    def __create_two_cycle_labeled_graph(
        dimensions: tuple[int, int], labels: tuple[str, str]
    ) -> MultiDiGraph:
        return cfpq_data.labeled_two_cycles_graph(
            n=dimensions[0], m=dimensions[1], labels=labels
        )

    @staticmethod
    def __run_hellings(cfg: CFG, graph: MultiDiGraph) -> list:
        wcnf = CFGManager.convert_cfg_to_wcnf(cfg)
        term_productions = {
            production for production in wcnf.productions if len(production.body) == 1
        }
        var_productions = {
            production for production in wcnf.productions if len(production.body) == 2
        }
        eps_productions = {
            production
            for production in wcnf.productions
            if len(production.body) not in (1, 2)
        }

        r1 = [
            (production.head, start_node, end_node)
            for production in term_productions
            for (start_node, end_node, label) in graph.edges(data="label")
            if label == production.body[0].value
        ]
        r2 = [
            (production.head, node, node)
            for production in eps_productions
            for node in graph.nodes
        ]
        r = r1 + r2

        m = r.copy()
        while m:
            (N, v, u) = m.pop()

            for (Ni, ui, vi) in r:
                if v == vi:
                    for production in var_productions:
                        closure = (production.head, ui, u)
                        if (
                            production.body[0] == Ni
                            and production.body[1] == N
                            and closure not in r
                        ):
                            r.append(closure)
                            m.append(closure)

            for (Ni, ui, vi) in r:
                if u == ui:
                    for production in var_productions:
                        closure = (production.head, v, vi)
                        if (
                            production.body[0] == N
                            and production.body[1] == Ni
                            and closure not in r
                        ):
                            r.append(closure)
                            m.append(closure)
        return r
