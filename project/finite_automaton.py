from pyformlang.finite_automaton import FiniteAutomaton, NondeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex
from networkx import MultiDiGraph


def regex_to_dfa(regex: str) -> FiniteAutomaton:
    eps_nfa = Regex(regex).to_epsilon_nfa()
    if eps_nfa is None:
        raise ValueError("Wrong regex format")
    return eps_nfa.to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph,
    start_states: set[int],
    final_states: set[int],
) -> NondeterministicFiniteAutomaton:
    eps_nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    nfa = eps_nfa.remove_epsilon_transitions()
    nodes = set(map(int, graph.nodes))
    start_states = start_states or nodes
    final_states = final_states or nodes

    for state in start_states:
        assert nfa.add_start_state(state)

    for state in final_states:
        assert nfa.add_final_state(state)

    return nfa
