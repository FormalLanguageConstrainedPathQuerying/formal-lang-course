from networkx import MultiDiGraph
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol


def create_automata(
    transitions: list[tuple[int, str, int]],
    start_states: list[int],
    final_states: list[int],
    automata: EpsilonNFA,
) -> EpsilonNFA:
    for state in map(lambda n: State(n), start_states):
        automata.add_start_state(state)
    for state in map(lambda n: State(n), final_states):
        automata.add_final_state(state)
    for state1_num, label, state2_num in transitions:
        automata.add_transition(State(state1_num), Symbol(label), State(state2_num))

    return automata


def create_graph(nodes: list[int], edges: list[tuple[int, str, int]]) -> MultiDiGraph:
    graph = MultiDiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(
        list(map(lambda edge: (edge[0], edge[2], {"label": edge[1]}), edges))
    )
    return graph
