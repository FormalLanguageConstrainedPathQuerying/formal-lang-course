import cfpq_data as cfpq
from networkx import MultiDiGraph


def create_labeled_two_cycles_graph(
    n: int, n_label: str, m: int, m_label: str
) -> MultiDiGraph:
    if not (n > 0 and m > 0):
        raise ValueError(f"Incorrect number of nodes! " f"n={n} and m={m} must be > 0")

    return cfpq.labeled_two_cycles_graph(n=n, m=m, labels=(n_label, m_label))
