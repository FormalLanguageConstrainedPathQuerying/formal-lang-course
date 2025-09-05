import cfpq_data

def get_node_num(name: str) -> int:
    bzip_path = cfpq_data.download(name)
    bzip = cfpq_data.graph_from_csv(bzip_path)
    num = bzip.number_of_nodes()
    return num

def get_edge_num(name: str) -> int:
    bzip_path = cfpq_data.download(name)
    bzip = cfpq_data.graph_from_csv(bzip_path)
    num = bzip.number_of_edges()
    return num

def get_labels(name: str) -> list[str]:
    bzip_path = cfpq_data.download(name)
    bzip = cfpq_data.graph_from_csv(bzip_path)
    labels = cfpq_data.get_sorted_labels(bzip.graph)
    return labels
