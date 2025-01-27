from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import EpsilonNFA, Symbol
from pyformlang.rsa import RecursiveAutomaton, Box
from typing import Optional, Dict, List
from functools import reduce

class AutomataOperations:
    @staticmethod
    def from_char(c: str) -> EpsilonNFA:
        if len(c) != 1:
            raise ValueError(f"Expected single character, got: '{c}'")
        return Regex(c).to_epsilon_nfa()

    @staticmethod
    def from_var(name: str) -> EpsilonNFA:
        return Regex(name.upper()).to_epsilon_nfa()

    @staticmethod
    def empty() -> EpsilonNFA:
        return Regex("$").to_epsilon_nfa()

    @staticmethod
    def minimize_operation(operation):
        def wrapper(*args, **kwargs):
            result = operation(*args, **kwargs)
            return result.minimize()

        return wrapper

    @staticmethod
    @minimize_operation
    def intersection(first: EpsilonNFA, second: EpsilonNFA) -> EpsilonNFA:
        return first.get_intersection(second)

    @staticmethod
    @minimize_operation
    def concat(first: EpsilonNFA, second: EpsilonNFA) -> EpsilonNFA:
        return first.concatenate(second)

    @staticmethod
    @minimize_operation
    def unite(first: EpsilonNFA, second: EpsilonNFA) -> EpsilonNFA:
        return first.union(second)

    @staticmethod
    def repeat_n_times(automaton: EpsilonNFA, n: int) -> EpsilonNFA:
        if n == 0:
            return AutomataOperations.empty()

        result = reduce(
            lambda acc, _: AutomataOperations.concat(acc, automaton),
            range(n - 1),
            automaton
        )
        return result.minimize()

    @staticmethod
    @minimize_operation
    def kleene_star(automaton: EpsilonNFA) -> EpsilonNFA:
        return automaton.kleene_star()

    @staticmethod
    def repeat_with_range(
            automaton: EpsilonNFA,
            min_repeats: int,
            max_repeats: Optional[int]
    ) -> EpsilonNFA:
        ops = AutomataOperations

        if min_repeats == 0 and max_repeats is None:
            return ops.kleene_star(automaton)

        if max_repeats is None:
            base = ops.repeat_n_times(automaton, min_repeats)
            star = ops.kleene_star(automaton)
            return ops.concat(base, star)

        if min_repeats == max_repeats:
            return ops.repeat_n_times(automaton, min_repeats)

        automata = [
            ops.repeat_n_times(automaton, i)
            for i in range(min_repeats, max_repeats + 1)
        ]
        return reduce(ops.unite, automata).minimize()

    @staticmethod
    def grouping(automaton: EpsilonNFA) -> EpsilonNFA:
        regex_str = f"({automaton.minimize().to_regex()})"
        return Regex(regex_str).to_epsilon_nfa()


class RSMBuilder:
    START_SYMBOL = "START"

    @staticmethod
    def build(
            main_automaton: EpsilonNFA,
            variable_automata: Dict[str, EpsilonNFA]
    ) -> RecursiveAutomaton:
        boxes: List[Box] = [
            Box(automaton, Symbol(name.upper()))
            for name, automaton in variable_automata.items()
        ]
        boxes.append(Box(main_automaton, Symbol(RSMBuilder.START_SYMBOL)))

        return RecursiveAutomaton(
            initial_label=Symbol(RSMBuilder.START_SYMBOL),
            boxes=boxes
        )


nfa_from_char = AutomataOperations.from_char
nfa_from_var = AutomataOperations.from_var
create_empty_nfa = AutomataOperations.empty
intersect = AutomataOperations.intersection
concatenate = AutomataOperations.concat
union = AutomataOperations.unite
repeat = AutomataOperations.repeat_n_times
kleene = AutomataOperations.kleene_star
repeat_range = AutomataOperations.repeat_with_range
group = AutomataOperations.grouping
build_rsm = RSMBuilder.build
START_TERMINAL_NAME = RSMBuilder.START_SYMBOL