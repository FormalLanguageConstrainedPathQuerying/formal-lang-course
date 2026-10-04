"""Convert regular expressions and labeled graphs to finite automata."""

from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import Regex


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    """Build a minimal DFA using pyformlang's regular expression syntax."""
    return Regex(regex).to_epsilon_nfa().to_deterministic().minimize()


def graph_to_nfa(
    graph: MultiDiGraph,
    start_states: set[int] | None = None,
    final_states: set[int] | None = None,
) -> NondeterministicFiniteAutomaton:
    """Keep graph vertices as states and edge labels as transition symbols.

    None or an empty boundary set selects all vertices, as required by the
    course tests. Isolated vertices are preserved. The graph is not modified.
    """
    starts = set(start_states) if start_states else set(graph.nodes)
    finals = set(final_states) if final_states else set(graph.nodes)
    if not (starts | finals) <= set(graph.nodes):
        raise ValueError("Start and final states must be graph vertices")

    automaton = NondeterministicFiniteAutomaton(
        states={State(node) for node in graph.nodes}
    )
    for node in starts:
        automaton.add_start_state(node)
    for node in finals:
        automaton.add_final_state(node)
    for source, target, data in graph.edges(data=True):
        automaton.add_transition(source, data["label"], target)
    return automaton
