from copy import deepcopy
import networkx as nx
from pyformlang.cfg import CFG
from pyformlang.rsa import RecursiveAutomaton
from project.task8 import cfg_to_rsm


def cfpq_with_gll(
    rsm: RecursiveAutomaton,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    if isinstance(rsm, CFG):
        rsm = cfg_to_rsm(rsm)

    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes

    initial_label = "S"
    if rsm.initial_label.value is not None:
        initial_label = rsm.initial_label.value

    start_nodes = {(initial_label, v) for v in start_nodes}
    stack_graph = {s: set() for s in start_nodes}
    visited = {
        (
            state[1],
            (initial_label, rsm.boxes[rsm.initial_label].dfa.start_state.value),
            state,
        )
        for state in start_nodes
    }
    queue = deepcopy(visited)

    def push(g_node, rsm_s, stack_s):
        s = (g_node, rsm_s, stack_s)
        if s not in visited:
            queue.add(s)
            visited.add(s)

    pop = {}
    result = set()
    while len(queue) > 0:
        graph_node, rsm_state, stack_state = queue.pop()

        if rsm_state[1] in rsm.boxes[rsm_state[0]].dfa.final_states:
            if stack_state in start_nodes:
                if graph_node in final_nodes:
                    result.add((stack_state[1], graph_node))
            pop.setdefault(stack_state, set()).add(graph_node)
            for ss, rs in stack_graph.setdefault(stack_state, set()):
                push(graph_node, rs, ss)

        ns = {}
        for _, u, l in graph.edges(graph_node, data="label"):
            ns.setdefault(l, set()).add(u)

        box_dfa_dict = rsm.boxes[rsm_state[0]].dfa.to_dict()
        if rsm_state[1] not in box_dfa_dict:
            continue
        for s, to in box_dfa_dict[rsm_state[1]].items():
            if s not in rsm.labels:
                if s.value not in ns:
                    continue
                for node in ns[s.value]:
                    push(node, (rsm_state[0], to.value), stack_state)
            else:
                ss = (s.value, graph_node)
                if ss in pop:
                    for gn in pop[ss]:
                        push(gn, (rsm_state[0], to.value), stack_state)
                stack_graph.setdefault(ss, set()).add(
                    (stack_state, (rsm_state[0], to.value))
                )
                push(graph_node, (s.value, rsm.boxes[s].dfa.start_state.value), ss)

    return result
