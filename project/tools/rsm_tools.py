from typing import Dict

import pyformlang
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State


def ebnf_to_rsm(ebnf: str) -> pyformlang.rsa.RecursiveAutomaton:
    return pyformlang.rsa.RecursiveAutomaton.from_text(ebnf)


def cfg_to_rsm(cfg: pyformlang.cfg.CFG) -> pyformlang.rsa.RecursiveAutomaton:
    return ebnf_to_rsm(cfg.to_text())


def rsm_to_nfa(
    rsm: pyformlang.rsa.RecursiveAutomaton,
) -> NondeterministicFiniteAutomaton:
    transitions = []
    start_states = set()
    fin_states = set()

    boxes: Dict[pyformlang.finite_automaton.Symbol, pyformlang.rsa.Box] = rsm.boxes
    for k in boxes:
        v = boxes[k]
        fa = v.dfa

        def new_state(s):
            return State((k, s))

        ss = set([new_state(s.value) for s in fa.start_states])
        start_states = start_states.union(ss)

        fs = set([new_state(s.value) for s in fa.final_states])
        fin_states = fin_states.union(fs)

        trs = fa.to_networkx().edges(data="label")
        for t in trs:
            transitions.append((new_state(t[0]), t[2], new_state(t[1])))

    res: NondeterministicFiniteAutomaton = NondeterministicFiniteAutomaton(
        start_state=start_states, final_states=fin_states
    )
    res.add_transitions(transitions)

    return res
