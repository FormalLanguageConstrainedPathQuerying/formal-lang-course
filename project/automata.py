from pyformlang.finite_automaton import DeterministicFiniteAutomaton as DFA
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton as NFA


def regex_to_dka(regex):
    return regex.to_epsilon_nfa().minimize()


def graph_to_nka(graph, bs, es):
    res = NFA(graph)
    for b in bs:
        res.add_start_state(b)
    for e in es:
        res.add_final_state(e)
    for v, u, data in graph.edges(data=True):
        print(data['label'])
        res.add_transition(v, Symbol(data['label']), u)
    return res