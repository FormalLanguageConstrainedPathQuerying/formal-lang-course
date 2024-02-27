from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from typing import Iterable, Any
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
) -> NondeterministicFiniteAutomaton:
    """Return nondeterministic finite automaton from :class:`nx.MultiDiGraph` graph

    Keyword arguments:
    graph -- source graph;
    starts -- `graph's` nodes marked as starts;
    finals -- `graph's` nodes marked as finals;
    """
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions([(v, d["label"], u) for v, u, d in graph.edges(data=True)])

    for node in starts:
        nfa.add_start_state(node)
    for node in finals:
        nfa.add_final_state(node)
    return nfa