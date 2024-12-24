from dataclasses import dataclass
from typing import Any, Iterable, Set, Tuple

from pyformlang.rsa import RecursiveAutomaton
from pyformlang.finite_automaton import State, Symbol
import networkx as nx


def get_graph_node_edges(g: nx.MultiDiGraph, from_nd):
    edges = {}
    for _, to_nd, lbl in g.edges(from_nd, data="label"):
        edges.setdefault(lbl, set()).add(to_nd)
    return edges


@dataclass
class RSMSt:
    nonterm: Symbol
    st: State

    def __hash__(self):
        return hash((self.nonterm, self.st))


def get_rsm_st_edges(
    rsm: RecursiveAutomaton, from_st: RSMSt
) -> dict[Symbol, Set[RSMSt]]:
    nonterm = from_st.nonterm
    edges = {}
    if rsm.get_box(nonterm) is None:
        return {}

    nonterm_edges = rsm.get_box(nonterm).dfa.to_dict()
    if from_st.st in nonterm_edges.keys():
        for lbl, to_st in nonterm_edges[from_st.st].items():
            if not isinstance(to_st, Iterable):
                edges.setdefault(lbl, set()).add(RSMSt(nonterm, to_st))
                continue

            for to_state in to_st:
                edges.setdefault(lbl, set()).add(RSMSt(nonterm, to_state))

    return edges


@dataclass
class GSSV:
    rsm_st: RSMSt
    graph_st: int

    def __hash__(self):
        return hash((self.rsm_st, self.graph_st))


@dataclass
class Config:
    rsm_st: RSMSt
    graph_st: int
    gss_v: GSSV

    def __hash__(self):
        return hash((self.rsm_st, self.graph_st, self.gss_v))


def get_new_configs(
    conf: Config,
    gss: nx.MultiDiGraph,
    graph: nx.DiGraph,
    rsm: RecursiveAutomaton,
    init_gss_v: GSSV,
) -> Tuple[Set[Config], Set[Tuple[int, int]]]:
    new_configs = set()
    graph_edges: dict[Any, Set[Any]] = get_graph_node_edges(
        nx.MultiDiGraph(graph), conf.graph_st
    )
    rsm_edges: dict[Symbol, Set[RSMSt]] = get_rsm_st_edges(rsm, conf.rsm_st)

    labels = set(graph_edges.keys()) & set(rsm_edges.keys())
    for lbl in labels:
        for rsm_st in rsm_edges[lbl]:
            for graph_st in graph_edges[lbl]:
                new_configs.add(Config(rsm_st, graph_st, conf.gss_v))

    POP_SET = "pop_set"
    for rsm_lbl in rsm_edges.keys():
        if rsm_lbl in rsm.labels:
            for rsm_start_st in rsm.get_box(rsm_lbl).start_state:
                new_rsm_st = RSMSt(rsm_lbl, rsm_start_st)
                new_gss_v = GSSV(new_rsm_st, conf.graph_st)

                if new_gss_v in gss.nodes and gss.nodes[new_gss_v][POP_SET]:
                    for graph_st in gss.nodes[new_gss_v][POP_SET]:
                        for rsm_st in rsm_edges[rsm_lbl]:
                            gss.add_edge(new_gss_v, conf.gss_v, label=rsm_st)
                            new_configs.add(Config(rsm_st, graph_st, conf.gss_v))
                    continue

                for rsm_st in rsm_edges[rsm_lbl]:
                    gss.add_node(new_gss_v, pop_set=None)
                    gss.add_edge(new_gss_v, conf.gss_v, label=rsm_st)

                new_configs.add(Config(new_rsm_st, conf.graph_st, new_gss_v))

    res = set()
    if conf.rsm_st.st in rsm.get_box(conf.rsm_st.nonterm).final_states:
        if gss.nodes[conf.gss_v][POP_SET] is None:
            gss.nodes[conf.gss_v][POP_SET] = set()
        gss.nodes[conf.gss_v][POP_SET].add(conf.graph_st)

        gss_edges: dict[RSMSt, Set[GSSV]] = get_graph_node_edges(gss, conf.gss_v)
        for lbl in gss_edges.keys():
            for gss_v in gss_edges[lbl]:
                if gss_v == init_gss_v:
                    res.add((conf.gss_v.graph_st, conf.graph_st))
                    continue
                new_configs.add(Config(lbl, conf.graph_st, gss_v))

    return new_configs, res


def gll_based_cfpq(
    rsm: RecursiveAutomaton,
    graph: nx.DiGraph,
    start_nodes: Set[int] = None,
    final_nodes: Set[int] = None,
) -> Set[tuple[int, int]]:
    if not start_nodes:
        start_nodes = set(graph.nodes)
    if not final_nodes:
        final_nodes = set(graph.nodes)

    queue: Set[Config] = set()
    processed_config: Set[Config] = set()
    GSS = nx.MultiDiGraph()
    init_gss_v = GSSV(RSMSt(Symbol("$"), State(0)), -1)

    for rsm_start in rsm.get_box(rsm.initial_label).start_state:
        for graph_st in start_nodes:
            rsm_st = RSMSt(rsm.initial_label, rsm_start)
            gss_v = GSSV(rsm_st, graph_st)

            GSS.add_node(gss_v, pop_set=None)
            GSS.add_edge(gss_v, init_gss_v, label=rsm_st)
            config = Config(rsm_st, graph_st, gss_v)
            queue.add(config)

    res = set()
    while queue:
        config = queue.pop()
        if config in processed_config:
            continue

        processed_config.add(config)
        new_configs, new_res = get_new_configs(config, GSS, graph, rsm, init_gss_v)
        queue |= new_configs
        res |= new_res

    return {
        (start_st, final_st)
        for start_st, final_st in res
        if start_st in start_nodes and final_st in final_nodes
    }
