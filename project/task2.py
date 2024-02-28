from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from typing import Iterable, Any, List
from pyformlang.regular_expression import Regex
import networkx as nx


def regex_to_dfa(expr: str) -> DeterministicFiniteAutomaton:
    """Return minimized DFA from regular expression string

    Keyword arguments:
    expr -- academic regular expression string;
    """
    dfa = Regex(expr).to_epsilon_nfa()
    return dfa.minimize()


def graph_to_nfa(
        graph: nx.MultiDiGraph,
        starts: Iterable[Any] = None,
        finals: Iterable[Any] = None,
) -> list[Any] | NondeterministicFiniteAutomaton:
    """Return nondeterministic finite automaton from :class:`nx.MultiDiGraph` graph

    Keyword arguments:
    graph -- source graph;
    starts -- `graph's` nodes marked as starts;
    finals -- `graph's` nodes marked as finals;
    """
    if not graph.edges() or (starts is None and finals is None):
        return []
    nfa = NondeterministicFiniteAutomaton()

    if starts is not None:
        for node in starts:
            nfa.add_start_state(node)
    if finals is not None:
        for node in finals:
            nfa.add_final_state(node)

    nfa.add_transitions([(v, d["label"], u) for v, u, d in graph.edges(data=True)])

    return nfa
