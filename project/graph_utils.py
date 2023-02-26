import cfpq_data


def get_graph(name):
    return cfpq_data.graph_from_csv(cfpq_data.download(name))


def get_labeled_two_cycle_graph(n, m, labels=("a", "b")):
    return cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
