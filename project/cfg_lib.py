import networkx as nx

from pyformlang.cfg import CFG, Terminal, Variable, Epsilon
from scipy.sparse import csc_matrix


def cfg_to_weak_normal_form(cfg: CFG) -> CFG:
    """
    Convert a CFG to weak Chomsky normal form.
    """
    if len(cfg.productions) == 0:
        return cfg

    new_cfg = (
        cfg.remove_useless_symbols()
        .eliminate_unit_productions()
        .remove_useless_symbols()
    )

    new_productions = new_cfg._get_productions_with_only_single_terminals()
    new_productions = new_cfg._decompose_productions(new_productions)

    return CFG(start_symbol=cfg.start_symbol, productions=set(new_productions))


def split_productions(productions):
    """
    Split WCNF productions into epsilon, terminal, and binary-non-terminal lookup structures.
    """
    epsilon_prods: set[Variable] = set()  # (A -> ε)
    term_prods: dict[Terminal, set[Variable]] = {}  # (A -> a)
    nonterm_prods: dict[(Variable, Variable), set[Variable]] = {}  # (A -> BC)

    for production in productions:
        head, body = production.head, production.body

        if len(body) == 0 or isinstance(body[0], Epsilon):
            epsilon_prods.add(head)
        elif len(body) == 1 and isinstance(body[0], Terminal):
            term_prods.setdefault(body[0].value, set()).add(head)
        else:
            nonterm_prods.setdefault((body[0], body[1]), set()).add(head)

    return epsilon_prods, term_prods, nonterm_prods


def hellings_based_cfpq(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    """
    Return all (u, v) pairs connected by a path whose labels derive from the CFG start symbol,
     via a Hellings-style fixed-point algorithm.
    """
    cfg = cfg_to_weak_normal_form(cfg)
    epsilon_prods, term_prods, nonterm_prods = split_productions(cfg.productions)

    adjacency_matrix = {(n, n, eps) for n in graph.nodes for eps in epsilon_prods} | {
        (start, final, term)
        for start, final, label in graph.edges.data("label")
        if label in term_prods
        for term in term_prods[label]
    }
    queue = adjacency_matrix.copy()

    while queue:
        new_nonterm = set()
        start1, final1, nonterm1 = queue.pop()

        for start2, final2, nonterm2 in adjacency_matrix:
            if final1 == start2 and (nonterm1, nonterm2) in nonterm_prods:
                for nonterm in nonterm_prods[(nonterm1, nonterm2)]:
                    if (start1, final2, nonterm) not in adjacency_matrix:
                        new_nonterm.add((start1, final2, nonterm))

            if final2 == start1 and (nonterm2, nonterm1) in nonterm_prods:
                for nonterm in nonterm_prods[(nonterm2, nonterm1)]:
                    if (start2, final1, nonterm) not in adjacency_matrix:
                        new_nonterm.add((start2, final1, nonterm))

        queue |= new_nonterm
        adjacency_matrix |= new_nonterm

    return {
        (start, final)
        for start, final, nonterm in adjacency_matrix
        if (
            start in start_nodes
            and final in final_nodes
            and nonterm.value == cfg.start_symbol.value
        )
    }


def matrix_based_cfpq(
    cfg: CFG,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    """
    Return (u, v) pairs from start_nodes to final_nodes connected by a path whose labels
     derive from the CFG start symbol, via matrix-based fixed-point iteration.
    """
    cfg = cfg_to_weak_normal_form(cfg)

    epsilon_prods, term_prods, nonterm_prods = split_productions(cfg.productions)
    node_to_idx = {n: i for i, n in enumerate(graph.nodes)}
    idx_to_node = {i: n for n, i in node_to_idx.items()}

    num_nodes = graph.number_of_nodes()
    adjacency_matrix: dict[Variable, csc_matrix] = {
        nonterm: csc_matrix((num_nodes, num_nodes), dtype=bool)
        for nonterm in cfg.variables
    }

    for eps in epsilon_prods:
        for n in range(num_nodes):
            adjacency_matrix[eps][n, n] = True

    for s, f, lbl in graph.edges.data("label"):
        if lbl in term_prods:
            for term in term_prods[lbl]:
                adjacency_matrix[term][node_to_idx[s], node_to_idx[f]] = True

    queue = set(cfg.variables)
    while queue:
        updated_var = queue.pop()

        for (
            M_B,
            M_C,
        ) in nonterm_prods:  # M_A = M_A + M_B * M_C, if A -> BC in nonterm_prods
            if updated_var != M_B and updated_var != M_C:
                continue

            matrix_change = adjacency_matrix[M_B] @ adjacency_matrix[M_C]
            for nonterm in nonterm_prods[(M_B, M_C)]:
                old_matrix = adjacency_matrix[nonterm]
                adjacency_matrix[nonterm] += matrix_change

                if (old_matrix != adjacency_matrix[nonterm]).count_nonzero() != 0:
                    queue.add(nonterm)

    valid_pairs: set[tuple[int, int]] = set()
    for nonterm in adjacency_matrix:
        if nonterm.value == cfg.start_symbol.value:
            for r, c in zip(*adjacency_matrix[nonterm].nonzero()):
                if idx_to_node[r] in start_nodes and idx_to_node[c] in final_nodes:
                    valid_pairs.add((idx_to_node[r], idx_to_node[c]))

    return valid_pairs
