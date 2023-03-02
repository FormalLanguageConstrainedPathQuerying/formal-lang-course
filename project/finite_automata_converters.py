from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol, Epsilon


class FAConverters(object):
    @classmethod
    def regex_to_min_dfa(cls, regex_str) -> DeterministicFiniteAutomaton:
        # Convert regex string to minimum DeterministicFiniteAutomaton
        regex = Regex(regex_str)
        nfa: EpsilonNFA = regex.to_epsilon_nfa()
        return nfa.minimize()

    @classmethod
    def graph_to_nfa(
        cls, graph: MultiDiGraph, start_nodes: set = None, finish_nodes: set = None
    ) -> NondeterministicFiniteAutomaton:
        # From MultiDiGraph and sets of start and finish nodes builds NondeterministicFiniteAutomaton
        if finish_nodes is None:
            finish_nodes = set(graph.nodes)
        if start_nodes is None:
            start_nodes = set(graph.nodes)

        nfa = NondeterministicFiniteAutomaton()

        for s in start_nodes:
            nfa.add_start_state(State(s))

        for s in finish_nodes:
            nfa.add_final_state(State(s))

        for s_from, s_to, d in graph.edges(data=True):
            symb_by = Symbol(d["label"]) if "label" in d else Epsilon
            nfa.add_transition(State(s_from), symb_by, State(s_to))

        return nfa
