from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix

from typing import Set, Tuple

from project.utils.CFG_utils import transform_cfg_to_wcnf, is_wcnf

__all__ = ["matrix_based"]


def matrix_based(cfg: CFG, graph: MultiDiGraph) -> Set[Tuple[int, str, int]]:
    """
    Matrix Based algorithm for Context Free Path Querying

    Parameters
    ----------
    cfg: CFG
        Query given in Context Free Grammar form
    graph: MultiDiGraph
        Labeled graph for the Path Querying task

    Returns
    -------
    r: set
        Set of triplets (node, variable, node)
    """
    wcnf = cfg if is_wcnf(cfg) else transform_cfg_to_wcnf(cfg)

    eps_prod_heads = [p.head.value for p in wcnf.productions if not p.body]
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}

    nodes_num = graph.number_of_nodes()
    matrices = {
        v.value: dok_matrix((nodes_num, nodes_num), dtype=bool) for v in wcnf.variables
    }

    for v_from, v_to, data in graph.edges(data=True):
        label = data["label"]
        for v in {p.head.value for p in term_productions if p.body[0].value == label}:
            matrices[v][v_from, v_to] = True

    for i in range(nodes_num):
        for v in eps_prod_heads:
            matrices[v][i, i] = True

    changed = True
    while changed:
        changed = False
        for p in var_productions:
            old_nnz = matrices[p.head.value].nnz
            matrices[p.head.value] += (
                matrices[p.body[0].value] @ matrices[p.body[1].value]
            )
            new_nnz = matrices[p.head.value].nnz
            changed = old_nnz != new_nnz

    return {
        (u, variable, v)
        for variable, matrix in matrices.items()
        for u, v in zip(*matrix.nonzero())
    }
