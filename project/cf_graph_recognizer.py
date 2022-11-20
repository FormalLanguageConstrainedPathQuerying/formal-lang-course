import networkx as nx
import pyformlang.cfg as c
from scipy import sparse
from project.cfg import cfg_to_wcnf


def matrix_based(graph: nx.Graph, cfg: c.CFG) -> set[tuple[int, c.Variable, int]]:
    cfg = cfg_to_wcnf(cfg)

    eps_prod_heads: set[c.Variable] = set()
    term_productions: dict[any, set[c.Variable]] = {}
    var_productions: set[tuple[c.Variable, c.Variable, c.Variable]] = set()
    for p in cfg.productions:
        match p.body:
            case [c.Epsilon()]:
                eps_prod_heads.add(p.head)
            case [c.Terminal() as t]:
                term_productions.setdefault(t.value, set()).add(p.head)
            case [c.Variable() as v1, c.Variable() as v2]:
                var_productions.add((p.head, v1, v2))

    nodes = {n: i for i, n in enumerate(graph.nodes)}
    adjs: dict[c.Variable, sparse.dok_array] = {
        v: sparse.dok_array((len(nodes), len(nodes)), dtype=bool) for v in cfg.variables
    }

    for n1, n2, l in graph.edges.data("label"):
        i = nodes[n1]
        j = nodes[n2]
        for v in term_productions.setdefault(l, set()):
            adjs[v][i, j] = True

    for adj in adjs.values():
        adj.tocsr()

    diag = sparse.csr_array(sparse.eye(len(nodes), dtype=bool))
    for v in eps_prod_heads:
        adjs[v] += diag

    changed = True
    while changed:
        changed = False
        for h, b1, b2 in var_productions:
            nnz_old = adjs[h].nnz
            adjs[h] += adjs[b1] @ adjs[b2]
            changed |= adjs[h].nnz != nnz_old

    nodes = {i: n for n, i in nodes.items()}
    result = set()
    for v, adj in adjs.items():
        for i, j in zip(*adj.nonzero()):
            result.add((nodes[i], v, nodes[j]))
    return result


def hellings(graph: nx.Graph, cfg: c.CFG) -> set[tuple[int, c.Variable, int]]:
    wcnf = cfg_to_wcnf(cfg)

    eps_prod_heads = [p.head.value for p in wcnf.productions if not p.body]
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    var_productions = {p for p in wcnf.productions if len(p.body) == 2}

    r = {(v, h, v) for v in range(graph.number_of_nodes()) for h in eps_prod_heads} | {
        (u, p.head.value, v)
        for u, v, edge_data in graph.edges(data=True)
        for p in term_productions
        if p.body[0].value == edge_data["label"]
    }

    new = r.copy()
    while new:
        n, N, m = new.pop()
        r_temp = set()

        for u, M, v in r:
            if v == n:
                triplets = {
                    (u, p.head.value, m)
                    for p in var_productions
                    if p.body[0].value == M
                    and p.body[1].value == N
                    and (u, p.head.value, m) not in r
                }
                r_temp |= triplets
        r |= r_temp
        new |= r_temp
        r_temp.clear()

        for u, M, v in r:
            if u == m:
                triplets = {
                    (n, p.head.value, v)
                    for p in var_productions
                    if p.body[0].value == N
                    and p.body[1].value == M
                    and (n, p.head.value, v) not in r
                }
                r_temp |= triplets
        r |= r_temp
        new |= r_temp

    return r
