import scipy.sparse as sp
from pyformlang.finite_automaton import EpsilonNFA


def to_matrices(e: EpsilonNFA, s2i: dict[any, int]) -> dict[str, sp.coo_matrix]:
    """

    takes EpsilonNFA and NodeName-to-Index dictionary
    returns dictionary of string keys and coo_matrix keys
    result is corresponding to coo_matrices for each label of EpsilonNFA

    """
    n = len(e.states)
    result = dict()

    def add(s, u, v):
        if s not in result:
            result[s] = sp.dok_matrix((n, n), dtype=bool)
        result[s][s2i[u], s2i[v]] = True

    for u, t in e.to_dict().items():
        for s, vs in t.items():
            if isinstance(vs, set):
                for v in vs:
                    add(s, u, v)
            else:
                add(s, u, vs)

    return result


def intersect(e1: EpsilonNFA, e2: EpsilonNFA):

    """

    takes 2 EpsilonNFA parameters and returns their intersection

    """

    s2i1 = {s: i for i, s in enumerate(e1.states)}
    s2i2 = {s: i for i, s in enumerate(e2.states)}
    m1 = to_matrices(e1, s2i1)
    m2 = to_matrices(e2, s2i2)
    sl = set.intersection(set(m1.keys()), set(m2.keys()))
    mr = {l: sp.kron(m1[l], m2[l]) for l in sl}

    r = EpsilonNFA()

    for l, b in mr.items():
        for i, j, v in zip(b.row, b.col, b.data):
            if v:
                r.add_transition(i, l, j)

    for ss1 in e1.start_states:
        for ss2 in e2.start_states:
            r.add_start_state(s2i1[ss1] * len(s2i2) + s2i2[ss2])

    for ss1 in e1.final_states:
        for ss2 in e2.final_states:
            r.add_final_state(s2i1[ss1] * len(s2i2) + s2i2[ss2])

    return r
