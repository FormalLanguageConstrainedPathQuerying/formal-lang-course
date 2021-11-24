from scipy.sparse import dok_matrix
from pyformlang.finite_automaton import State
from pyformlang.cfg import Variable

from project.grammars.rsm_box import RSMBox
from project.grammars.rsm import RSM

from project.utils.boolean_matrix import BooleanMatrix

__all__ = ["RSMMatrix"]


class RSMMatrix(BooleanMatrix):
    def __init__(self):
        super().__init__()

    @staticmethod
    def rename_rsm_box_state(state: State, box_variable: Variable):
        return State(f"{state.value}#{box_variable.value}")

    @classmethod
    def from_rsm(cls, rsm: RSM):
        bm = cls()
        bm.number_of_states = sum(len(box.dfa.states) for box in rsm.boxes)
        box_idx = 0
        for box in rsm.boxes:
            for idx, state in enumerate(box.dfa.states):
                new_name = bm.rename_rsm_box_state(state, box.variable)
                bm.indexed_states[new_name] = idx + box_idx
                if state in box.dfa.start_states:
                    bm.start_states.add(bm.indexed_states[new_name])
                if state in box.dfa.final_states:
                    bm.final_states.add(bm.indexed_states[new_name])

            bm.states_to_box_variable.update(
                {
                    (
                        bm.indexed_states[
                            bm.rename_rsm_box_state(box.dfa.start_state, box.variable)
                        ],
                        bm.indexed_states[bm.rename_rsm_box_state(state, box.variable)],
                    ): box.variable.value
                    for state in box.dfa.final_states
                }
            )
            bm.bmatrix.update(bm._create_box_bool_matrices(box))
            box_idx += len(box.dfa.states)

        return bm

    def get_nonterminals(self, s_from, s_to):
        return self.states_to_box_variable.get((s_from, s_to))

    def _create_box_bool_matrices(self, box: RSMBox):
        bmatrix = {}
        for s_from, trans in box.dfa.to_dict().items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for s_to in states_to:
                    idx_from = self.indexed_states[
                        self.rename_rsm_box_state(s_from, box.variable)
                    ]
                    idx_to = self.indexed_states[
                        self.rename_rsm_box_state(s_to, box.variable)
                    ]
                    label = str(label)
                    if label in self.bmatrix:
                        self.bmatrix[label][idx_from, idx_to] = True
                        continue
                    if label not in bmatrix:
                        bmatrix[label] = dok_matrix(
                            (self.number_of_states, self.number_of_states)
                        )
                    bmatrix[label][idx_from, idx_to] = True

        return bmatrix
