from typing import Set

import pyformlang.regular_expression as re
import pyformlang.finite_automaton as fa
import networkx as nx

# Используя возможности pyformlang реализовать функцию построения минимального ДКА по заданному регулярному выражению.


def regex_to_dfa(regex: re.Regex) -> fa.DeterministicFiniteAutomaton:
    nfa = regex.to_epsilon_nfa()
    return nfa.minimize().to_deterministic()


# Используя возможности pyformlang реализовать функцию построения недетерминированного конечного автомата по графу,
# в том числе по любому из графов, которые можно получить, пользуясь функциональностью, реализованной в Задаче 1
# (загруженный из набора данных по имени граф, сгенерированный синтетический граф). Предусмотреть возможность указывать
# стартовые и финальные вершины. Если они не указаны, то считать все вершины стартовыми и финальными.
def graph_to_nfa(
    graph: nx.MultiGraph, start_states: Set = None, final_states: Set = None
) -> fa.NondeterministicFiniteAutomaton:
    all_nodes = set(graph)

    if start_states is None:
        start_states = all_nodes

    if final_states is None:
        final_states = all_nodes

    if not start_states.issubset(all_nodes):
        raise AttributeError(
            f"Start states are invalid: {start_states.difference(all_nodes)}"
        )
    if not final_states.issubset(all_nodes):
        raise AttributeError(
            f"Final states are invalid: {final_states.difference(all_nodes)}"
        )

    nfa = fa.NondeterministicFiniteAutomaton(states=all_nodes)

    for st in start_states:
        nfa.add_start_state(fa.State(st))
    for st in final_states:
        nfa.add_final_state(fa.State(st))

    for fr, to, label in graph.edges(data="label"):
        nfa.add_transition(fa.State(fr), fa.Symbol(label), fa.State(to))

    return nfa
