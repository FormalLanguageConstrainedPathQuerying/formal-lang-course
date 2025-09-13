from typing import Optional, Set
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State, Symbol
from networkx import MultiDiGraph

def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    rx = Regex(regex)
    nfa = rx.to_epsilon_nfa()
    return nfa.to_deterministic()


def graph_to_nfa(
    graph: MultiDiGraph,
    start_states: Optional[Set[int]] = None,
    final_states: Optional[Set[int]] = None,
) -> NondeterministicFiniteAutomaton:

    nfa = NondeterministicFiniteAutomaton()

    graph_nodes = set(graph.nodes())
    if not start_states:
        start_states = set(graph_nodes)
    if not final_states:
        final_states = set(graph_nodes)

    for s in start_states:
        nfa.add_start_state(State(s))
    for f in final_states:
        nfa.add_final_state(State(f))

    # helper to pick label from edge data
    def _extract_label(data):
        if data is None:
            return None

        if not isinstance(data, dict):
            return data

        for key in ("label", "symbol", "weight"):
            if key in data:
                return data[key]

        if len(data) == 1:
            return next(iter(data.values()))

        return None

    for u, v, key, data in graph.edges(keys=True, data=True):
        label = _extract_label(data)

        if label is None or (isinstance(label, str) and label == ""):
            nfa.add_transition(State(u), None, State(v))
        else:
            sym = Symbol(str(label))
            nfa.add_transition(State(u), sym, State(v))

    return nfa
