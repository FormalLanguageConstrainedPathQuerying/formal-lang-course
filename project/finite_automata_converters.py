from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol, Epsilon


class FAConverters(object):
    """Class FAConverters transforms regex to DFA, graph to NFA.

    Methods
    -------
    regex_to_min_dfa(regex_str)
        Convert regex string to minimum DeterministicFiniteAutomaton.

    graph_to_nfa(cls, graph: MultiDiGraph, start_nodes: set = None, finish_nodes: set = None)
        From MultiDiGraph and sets of start and finish nodes builds NondeterministicFiniteAutomaton.
    """

    @classmethod
    def regex_to_min_dfa(cls, regex_str: str) -> DeterministicFiniteAutomaton:
        """

        Convert regex string to minimum DeterministicFiniteAutomaton.
        @type regex_str: string with regex.
        @rtype: DeterministicFiniteAutomaton which is build with regex_str.
        """
        regex = Regex(regex_str)
        nfa: EpsilonNFA = regex.to_epsilon_nfa()
        return nfa.minimize()

    @classmethod
    def graph_to_nfa(
        cls, graph: MultiDiGraph, start_nodes: set = None, finish_nodes: set = None
    ) -> NondeterministicFiniteAutomaton:
        """

        From MultiDiGraph and sets of start and finish nodes builds NondeterministicFiniteAutomaton.
        @param graph: input graph for transforming.
        @param start_nodes: set of nodes, which should be start. If is None all nodes will be start.
        @param finish_nodes: set of nodes, which should be finish. If is None all nodes will be finish.
        @return: NondeterministicFiniteAutomaton which is build from graph.
        """
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
