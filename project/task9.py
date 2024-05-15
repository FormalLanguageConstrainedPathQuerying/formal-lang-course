from project.task8 import cfg_to_rsm

from pyformlang.cfg import CFG
import networkx as nx
from pyformlang.finite_automaton import Symbol, State
from copy import deepcopy
from pyformlang.rsa import RecursiveAutomaton


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

    rsm_start_nonterm = rsm.initial_label.value

    stack_start_states = set()
    for sn in start_nodes:
        stack_start_states.add((rsm_start_nonterm, sn))

    stack = dict()
    for state in stack_start_states:
        stack[state] = set()

    rsm_start = rsm.boxes[rsm.initial_label].dfa.start_state.value

    visited = set()
    for state in stack_start_states:
        visited.add(((rsm_start_nonterm, rsm_start), state[1], state))

    res = set()
    removed = {}
    to_visit = deepcopy(visited)

    while len(to_visit) != 0:
        rsm_state, graph_node, stack_state = to_visit.pop()

        if State(rsm_state[1]) in rsm.boxes[rsm_state[0]].dfa.final_states:
            if stack_state in stack_start_states:
                if graph_node in final_nodes:
                    res.add((stack_state[1], graph_node))

            if stack_state not in removed.keys():
                removed[stack_state] = set()
            removed[stack_state].add(graph_node)
            for to_stack_state, to_rsm_state in stack.setdefault(stack_state, set()):
                new = (to_rsm_state, graph_node, to_stack_state)
                if new not in visited:
                    to_visit.add(new)
                    visited.add(new)

        to_nodes = {}
        for q, a, b in graph.edges(graph_node, data="label"):
            if b not in to_nodes.keys():
                to_nodes[b] = set()
            to_nodes[b].add(a)

        dfa_dict = rsm.boxes[Symbol(rsm_state[0])].dfa.to_dict()
        if State(rsm_state[1]) not in dfa_dict:
            continue
        for symb, to in dfa_dict[State(rsm_state[1])].items():
            if symb in rsm.labels:
                new_state_on_stack = (symb.value, graph_node)
                if new_state_on_stack in removed:
                    for to_graph_node in removed[new_state_on_stack]:
                        new = (
                            (rsm_state[0], to.value),
                            to_graph_node,
                            stack_state,
                        )
                        if new not in visited:
                            to_visit.add(new)
                            visited.add(new)

                if new_state_on_stack not in stack.keys():
                    stack[new_state_on_stack] = set()
                stack[new_state_on_stack].add((stack_state, (rsm_state[0], to.value)))

                start_state = rsm.boxes[symb].dfa.start_state.value
                new = ((symb.value, start_state), graph_node, new_state_on_stack)
                if new not in visited:
                    to_visit.add(new)
                    visited.add(new)
            else:
                if symb.value not in to_nodes:
                    continue
                for node in to_nodes[symb.value]:
                    new = ((rsm_state[0], to.value), node, stack_state)
                    if new not in visited:
                        to_visit.add(new)
                        visited.add(new)

    ans = set()
    for i in res:
        if i[0] != i[1]:
            ans.add(i)
    return ans
