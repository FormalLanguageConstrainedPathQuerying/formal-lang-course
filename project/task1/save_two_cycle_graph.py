import cfpq_data, networkx
from typing import Tuple

def save_two_cycle_graph(n: int, m: int, labels: Tuple[str, str], name: str) -> bool:
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    dotgraph = networkx.drawing.nx_pydot.to_pydot(graph)
    dotgraph.write_raw(name + ".dot")
    return True
