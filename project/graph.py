import cfpq_data
import networkx

def get_graph_info(name: str):
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)
    print('\n', graph.number_of_nodes(), graph.number_of_edges(), cfpq_data.get_sorted_labels(graph), '\n')
    return graph.number_of_nodes(), graph.number_of_edges(), cfpq_data.get_sorted_labels(graph)

def create_two_cycle_graph(n, m, labels, path):
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    networkx.drawing.nx_pydot.write_dot(graph, path)

# get_graph_info("bzip")
# create_two_cycle_graph(3, 2, ["a", "b"], "a.dot")
