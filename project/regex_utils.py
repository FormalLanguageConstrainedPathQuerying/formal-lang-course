import networkx as nx
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
    Symbol,
    EpsilonNFA,
    Epsilon,
)
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: str | Regex) -> DeterministicFiniteAutomaton:
    if not isinstance(regex, Regex):
        regex = Regex(regex)
    min_dfa = regex.to_epsilon_nfa().minimize()
    return min_dfa


def create_automaton(start_states, final_states, transitions, automaton) -> EpsilonNFA:
    for state in map(lambda n: State(n), start_states):
        automaton.add_start_state(state)

    for state in map(lambda n: State(n), final_states):
        automaton.add_final_state(state)

    for state_from, label, state_to in transitions:
        automaton.add_transition(State(state_from), Symbol(label), State(state_to))

    return automaton


def graph_to_nfa(
    graph: nx.Graph,
    start_states: set | None = None,
    final_states: set | None = None,
) -> EpsilonNFA:
    enfa = EpsilonNFA()

    # Only iterating through edges as isolated nodes can be either start or final and
    # thus will be added later anyway
    for pred, succ, data in graph.edges.data():
        pred_state = State(pred)
        succ_state = State(succ)
        symbol = Symbol(data["label"]) if "label" in data else Epsilon
        enfa.add_transition(pred_state, symbol, succ_state)

    if start_states is None:
        start_states = set(graph.nodes)
    if final_states is None:
        final_states = set(graph.nodes)

    for state in start_states:
        enfa.add_start_state(state)
    for state in final_states:
        enfa.add_final_state(state)

    return enfa


def create_nfa_from_graph(
    graph: nx.Graph, start_states: set = None, final_states: set = None
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for statement_from, statement_to, transition in graph.edges(data=True):
        nfa.add_transition(
            State(int(statement_from)),
            Symbol(transition["label"]),
            State(int(statement_to)),
        )

    for node in map(lambda node: int(node), graph.nodes):
        if not start_states or node in map(lambda state: int(state), start_states):
            nfa.add_start_state(State(node))
        if not final_states or node in map(lambda state: int(state), final_states):
            nfa.add_final_state(State(node))

    return nfa


def create_graph(nodes: list, edges: list[tuple[any, any, any]]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(
        list(map(lambda edge: (edge[0], edge[2], {"label": edge[1]}), edges))
    )

    return graph
