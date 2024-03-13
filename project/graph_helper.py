import cfpq_data as data
import networkx as nx
from networkx import MultiDiGraph

# ['skos', 'wc', 'generations', 'travel', 'univ', 'atom', 'biomedical', 'bzip',
# 'foaf', 'people', 'pr', 'funding', 'ls', 'wine', 'pizza', 'gzip', 'core', 'pathways',
# 'enzyme', 'eclass', 'go_hierarchy', 'go', 'apache', 'init', 'mm', 'geospecies', 'ipc',
# 'lib', 'block', 'arch', 'crypto', 'security', 'sound', 'net', 'fs', 'drivers', 'postgre',
# 'kernel', 'taxonomy', 'taxonomy_hierarchy', 'avrora', 'batik', 'eclipse', 'fop', 'h2',
# 'jython', 'luindex', 'lusearch', 'pmd', 'sunflow', 'tomcat', 'tradebeans', 'tradesoap', 'xalan']


def get_graph_by_name(name: str) -> MultiDiGraph:
    graph_csv = data.download(name)
    return data.graph_from_csv(graph_csv)


def get_graph_info(graph: MultiDiGraph) -> dict:
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "nodes_list": list(graph.nodes),
        "edges_list": list(graph.edges),
    }


def export2_dot_file(graph: MultiDiGraph, path: str) -> None:
    nx.drawing.nx_pydot.write_dot(graph, path)


# По количеству вершин в циклах и именам меток строить граф из
# двух циклов и сохранять его в указанный файл в формате DOT (использовать pydot)
def build_graph_and_save_to_dot_file(
    cycles: list[int], labels: list[str], path: str
) -> MultiDiGraph:
    graph = nx.MultiDiGraph()
    graph.add_edge(cycles[0], cycles[1], label=labels[0])
    graph.add_edge(cycles[1], cycles[0], label=labels[1])
    export2_dot_file(graph, path)
    return graph
