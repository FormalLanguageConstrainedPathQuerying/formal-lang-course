from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton as Automata, State
import networkx as nx
import cfpq_data


# Creates Deterministic Finite Automata from Regex
def regex_to_dka(regex):
    return regex.to_epsilon_nfa().minimize()


# Creates Nondeterministic Automata from MultiDiGraph, begin nodes list, end nodes list
def graph_to_nka(graph, bs, es):
    res = Automata(graph)
    for b in bs:
        res.add_start_state(b)
    for e in es:
        res.add_final_state(e)
    for v, u, data in graph.edges(data=True):
        print(data["label"])
        res.add_transition(v, Symbol(data["label"]), u)
    return res


def get_graph(name):
    return cfpq_data.graph_from_csv(cfpq_data.download(name))


def build_dfa_from_graph(
        graph: nx.DiGraph, start: set[State] = None, final: set[State] = None
) -> Automata:
    """
    Builds NDFA from graph representation, start and final nodes
    :param graph: Graph representation of the resulting NDFA
    :param start: Start states of the resulting NDFA. If None - all states are considered start states
    :param final: Final states of the resulting NDFA. If None - all states are considered final states
    :return: NDFA built from graph representation, start and final nodes
    """
    dfa = Automata.from_networkx(graph)

    for s, f, label in graph.edges(data="label"):
        dfa.add_transition(s, label, f)

    if start is not None:
        for s in start:
            dfa.add_start_state(s)
    else:
        for s in dfa.states:
            dfa.add_start_state(s)
    if final is not None:
        for s in final:
            dfa.add_final_state(s)
    else:
        for s in dfa.states:
            dfa.add_final_state(s)

    return dfa
