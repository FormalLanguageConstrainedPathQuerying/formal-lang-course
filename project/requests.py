import scipy.sparse as sp
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.regular_expression import Regex
from networkx.classes.multidigraph import MultiDiGraph

from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton as NFA


# Creates Deterministic Finite Automata from Regex
def regex_to_dka(regex: Regex) -> EpsilonNFA:
    return regex.to_epsilon_nfa().minimize()


# Creates Nondeterministic Automata from MultiDiGraph, begin nodes list, end nodes list
def graph_to_nka(graph: any, bs: list[State], es: list[State]) -> NFA:
    res = NFA(graph)
    for b in bs:
        res.add_start_state(b)
    for e in es:
        res.add_final_state(e)
    for v, u, data in graph.edges(data=True):
        res.add_transition(v, Symbol(data["label"]), u)
    return res


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


def print_nfa(e, s):
    print(s)
    for s1, d in e.to_dict().items():
        for _, s2 in d.items():
            if isinstance(s2, State):
                print(s1, '-', s2)
            else:
                for sa in s2:
                    print(s1, '-', sa)


def intersect(e1: EpsilonNFA, e2: EpsilonNFA) -> EpsilonNFA:

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
            r.add_start_state(s2i1[ss1] * s2i2[ss2])

    for fs1 in e1.final_states:
        for fs2 in e2.final_states:
            r.add_final_state(s2i1[fs1] * s2i2[fs2])

    return r


def graph_request(graph: MultiDiGraph, start_nodes: list[State], end_nodes: list[State], regex: Regex) -> set[(State, State)]:
    nfa = graph_to_nka(graph, start_nodes, end_nodes)
    req = regex_to_dka(regex)
    e = intersect(nfa, req)
    res = set()
    g = MultiDiGraph()

    i = 0
    a = dict()
    for s in e.states:
        a[s] = i
        i += 1

    for s in e.states:
        g.add_node(s)

    for s1, d in e.to_dict().items():
        for _, vs in d.items():
            for s2 in vs:
                print('S1:', a[s1], '; S2:', a[s2])
                g.add_edge(a[s1], a[s2])

    n = g.number_of_nodes()

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if g.has_edge(i, k) and g.has_edge(k, j):
                    g.add_edge(i, j)

    for s in e.start_states:
        print('S:', s)
        for f in e.final_states:
            print('F:', f)
            if g.has_edge(a[s], a[f]):
                res.add((s, f))

    return res
