from cfpq_data import graph_from_csv, download
from networkx import Graph
from networkx.drawing.nx_pydot import to_pydot


class GraphWorker:
    def __init__(self):
        self.__graph_info = {"num_of_nodes": 0,
                             "num_of_edges": 0,
                             "set_of_labels": set()
                             }
        self.__graph = Graph()

    def __update_graph_info(self) -> None:
        self.__graph_info["num_of_nodes"] = self.__graph.number_of_nodes()
        self.__graph_info["num_of_edges"] = self.__graph.number_of_edges()
        self.__graph_info["set_of_labels"] = {label
                                              for _, _, label
                                              in self.__graph.edges.data("label")
                                              }

    def load_graph_by_name(self, name: str) -> None:
        self.__graph = graph_from_csv(path=download(name))
        self.__update_graph_info()

    def update_graph(self, graph: Graph) -> None:
        self.__graph = graph
        self.__update_graph_info()

    def get_graph_info(self) -> dict:
        return self.__graph_info

    def save_as_dot_file(self, path: str) -> bool:
        return to_pydot(self.__graph).write(path)


if __name__ == "__main__":
    gw = GraphWorker()
    gw.load_graph_by_name("bzip")
    gw.save_as_dot_file('test.dot')
    print(gw.get_graph_info())
