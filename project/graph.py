import cfpq_data
import networkx as nx


def get_graph_info(name):
    graph = cfpq_data.graph_from_csv(cfpq_data.download(name))

    s = set()
    for i in dict(graph.edges).values():
        for j in i.values():
            s.add(j)

    return graph.number_of_nodes(), graph.number_of_edges(), s


def two_cycles_graph_to_file(n1, n2, labels, filename):
    g = cfpq_data.graphs.generators.labeled_two_cycles_graph(n1, n2, labels=labels)
    graph = nx.drawing.nx_pydot.to_pydot(g)
    graph.write(filename)
