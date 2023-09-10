import cfpq_data
import networkx


def load_graph(graph_name: str) -> networkx.MultiDiGraph:
    return cfpq_data.graph_from_csv(cfpq_data.download(graph_name))
