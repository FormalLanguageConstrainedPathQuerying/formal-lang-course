from typing import Dict, Set

from project.task3.finite_automaton import (
    FiniteAutomaton,
    intersect_automata,
    transitive_closure,
)


def reachability_with_constraints(
    fa: FiniteAutomaton, constraints_fa: FiniteAutomaton
) -> Dict[int, Set[int]]:
    """
    Вычисляет достижимость состояний в КА с учетом ограничений.

    Функция принимает два конечных автомата: исходный автомат и автомат ограничений.
    Она вычисляет пересечение этих автоматов, находит транзитивное замыкание полученного
    пересеченного автомата и определяет достижимые состояния для начальных состояний
    исходного автомата с учетом ограничений.

    Аргументы:
    - fa (FiniteAutomaton): Исходный конечный автомат.
    - constraints_fa (FiniteAutomaton): Конечный автомат, задающий ограничения.
    """
    inter = intersect_automata(fa, constraints_fa, lbl=False)

    closure = transitive_closure(inter)

    map_states = {v: i for i, v in fa.states_to_states.items()}
    con_len = len(constraints_fa.states_to_states)
    reachability = dict()

    for start in fa.start_states:
        reachability[start] = set()

    for v, u in zip(*closure.nonzero()):
        if v in inter.start_states and u in inter.final_states:
            reachability[map_states[v // con_len]].add(map_states[u // con_len])

    return reachability
