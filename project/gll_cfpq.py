from dataclasses import dataclass, field
from pyformlang.rsa import RecursiveAutomaton
from networkx import DiGraph, MultiDiGraph
from pyformlang.finite_automaton import State, Symbol
from typing import Optional, Any, Iterable


@dataclass(frozen=True, eq=True)
class RsmState:
    nonterm: Symbol
    state: State


@dataclass
class GSSNode:
    rsm_st: RsmState
    graph_st: int
    pop_set: set[int] = field(default_factory=set)

    def __hash__(self):
        return hash((self.rsm_st, self.graph_st))

    def __eq__(self, other):
        return self.rsm_st == other.rsm_st and self.graph_st == other.graph_st


@dataclass(frozen=True, eq=True)
class Configuration:
    rsm_st: RsmState
    graph_st: int
    gss_node: GSSNode


class GLLSolver:
    def __init__(self, rsm: RecursiveAutomaton, graph: DiGraph):
        self.rsm = rsm
        self.graph = graph
        self.queue: set[Configuration] = set()
        self.processed_config: set[Configuration] = set()
        self.gss: MultiDiGraph = MultiDiGraph()
        self.init_gss = GSSNode(RsmState(Symbol("$"), State("fin")), -1)

    def solve(
        self, start_nodes: set[int], final_nodes: set[int]
    ) -> set[tuple[int, int]]:

        res: set[tuple[int, int]] = set()

        for rsm_start in self.rsm.get_box(self.rsm.initial_label).start_state:
            for graph_st in start_nodes:
                rsm_st = RsmState(self.rsm.initial_label, rsm_start)
                node = GSSNode(rsm_st, graph_st)

                self.gss.add_node(node)
                self.gss.add_edge(node, self.init_gss, label=rsm_st)
                config = Configuration(rsm_st, graph_st, node)
                self.queue.add(config)

        while self.queue:
            config = self.queue.pop()
            if config in self.processed_config:
                continue

            self.processed_config.add(config)
            self.queue |= self.get_new_configurations(config, res)

        return {
            (start, final)
            for start, final in res
            if start in start_nodes and final in final_nodes
        }

    def get_new_configurations(
        self,
        conf: Configuration,
        res: set[tuple[int, int]],
    ) -> set[Configuration]:
        new_configurations = set()
        graph_edges: dict[Any, set[Any]] = get_graph_node_edges(
            MultiDiGraph(self.graph), conf.graph_st
        )
        rsm_edges: dict[Symbol, set[RsmState]] = get_rsm_from_state_edges(
            self.rsm, conf.rsm_st
        )

        labels = set(graph_edges.keys()) & set(rsm_edges.keys())
        for lbl in labels:
            for rsm_st in rsm_edges[lbl]:
                for graph_st in graph_edges[lbl]:
                    new_configurations.add(
                        Configuration(rsm_st, graph_st, conf.gss_node)
                    )

        for rsm_lbl in rsm_edges.keys():
            if rsm_lbl in self.rsm.labels:
                for rsm_start_st in self.rsm.get_box(rsm_lbl).start_state:
                    new_rsm_st = RsmState(rsm_lbl, rsm_start_st)
                    new_node = GSSNode(new_rsm_st, conf.graph_st)

                    if new_node in self.gss.nodes:
                        for n in self.gss.nodes:
                            if n == new_node:
                                new_node = n

                    if new_node in self.gss.nodes and new_node.pop_set:
                        for graph_st in new_node.pop_set:
                            for rsm_st in rsm_edges[rsm_lbl]:
                                self.gss.add_edge(new_node, conf.gss_node, label=rsm_st)
                                new_configurations.add(
                                    Configuration(rsm_st, graph_st, conf.gss_node)
                                )
                        continue

                    for rsm_st in rsm_edges[rsm_lbl]:
                        self.gss.add_node(new_node)
                        self.gss.add_edge(new_node, conf.gss_node, label=rsm_st)

                    new_configurations.add(
                        Configuration(new_rsm_st, conf.graph_st, new_node)
                    )

        if conf.rsm_st.state in self.rsm.get_box(conf.rsm_st.nonterm).final_states:
            conf.gss_node.pop_set.add(conf.graph_st)

            gss_edges: dict[RsmState, set[GSSNode]] = get_graph_node_edges(
                self.gss, conf.gss_node
            )
            for lbl in gss_edges.keys():
                for gss_v in gss_edges[lbl]:
                    if gss_v == self.init_gss:
                        res.add((conf.gss_node.graph_st, conf.graph_st))
                        continue
                    new_configurations.add(Configuration(lbl, conf.graph_st, gss_v))

        return new_configurations


def gll_based_cfpq(
    rsm: RecursiveAutomaton,
    graph: DiGraph,
    start_nodes: Optional[set[int]] = None,
    final_nodes: Optional[set[int]] = None,
) -> set[tuple[int, int]]:
    start_nodes = start_nodes or set(graph.nodes)
    final_nodes = final_nodes or set(graph.nodes)

    solver = GLLSolver(rsm, graph)
    return solver.solve(start_nodes, final_nodes)


def get_graph_node_edges(g: MultiDiGraph, nodes: Any) -> dict[Any, set[Any]]:
    edges: dict[Any, set[Any]] = {}
    lbl: Any
    for _, finish, lbl in g.edges(nodes, data="label"):
        edges.setdefault(lbl, set()).add(finish)
    return edges


def get_rsm_from_state_edges(
    rsm: RecursiveAutomaton, from_st: RsmState
) -> dict[Symbol, set[RsmState]]:
    box_label = from_st.nonterm
    dfa = rsm.get_box(box_label).dfa
    edges: dict[Symbol, set[RsmState]] = {}
    if from_st.state not in dfa.to_dict():
        return {}

    for label, to_states in (dfa.to_dict()[from_st.state]).items():
        if not isinstance(to_states, Iterable):
            edges.setdefault(label, set()).add(RsmState(box_label, to_states))
            continue

        for to_state in to_states:
            edges.setdefault(label, set()).add(RsmState(box_label, to_state))

    return edges
