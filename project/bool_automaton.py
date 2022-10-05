from pyformlang.finite_automaton import FiniteAutomaton
from scipy.sparse import dok_matrix, kron, block_diag, vstack


class BoolAutomaton:
    def __init__(self, automaton: FiniteAutomaton):
        self.start_states = automaton.start_states
        self.final_states = automaton.final_states
        self.number_of_states = len(automaton.states)
        self.edges = dict()
        self.state_number = dict()
        self.state_number = {
            state: index for index, state in enumerate(automaton.states)
        }

        transitions = automaton.to_dict()

        for from_state in transitions.keys():
            for label in transitions.get(from_state).keys():
                if not isinstance(transitions.get(from_state).get(label), set):
                    transitions.get(from_state)[label] = {
                        transitions.get(from_state).get(label)
                    }
                for to_state in transitions.get(from_state).get(label):
                    if label not in self.edges.keys():
                        self.edges[label] = dok_matrix(
                            (self.number_of_states, self.number_of_states), dtype=bool
                        )
                    i = self.state_number.get(from_state)
                    j = self.state_number.get(to_state)
                    self.edges[label][i, j] = True

    def intersect(self, target_automaton):
        labels = set(self.edges.keys()).intersection(set(target_automaton.edges.keys()))
        intersection_edges = dict()
        for label in labels:
            intersection_edges[label] = kron(
                self.edges[label], target_automaton.edges[label]
            )
        start_states = set()
        final_states = set()
        for start1 in self.start_states:
            for start2 in target_automaton.start_states:
                start_states.add(
                    self.state_number.get(start1) * target_automaton.number_of_states
                    + target_automaton.state_number.get(start2)
                )

        for final1 in self.final_states:
            for final2 in target_automaton.final_states:
                final_states.add(
                    self.state_number.get(final1) * target_automaton.number_of_states
                    + target_automaton.state_number.get(final2)
                )

        return self.create_bool_automaton(
            intersection_edges, start_states, final_states
        )

    @classmethod
    def create_bool_automaton(cls, intersection_edges, start_states, final_states):
        bool_automaton = super(BoolAutomaton, cls).__new__(cls)
        bool_automaton.edges = intersection_edges
        bool_automaton.start_states = start_states
        bool_automaton.final_states = final_states
        return bool_automaton

    def transitive_closure(self):
        adj_matrix = sum(self.edges.values())
        prev_nnz = adj_matrix.nnz
        cur_nnz = 0
        while prev_nnz != cur_nnz:
            adj_matrix += adj_matrix @ adj_matrix
            prev_nnz = cur_nnz
            cur_nnz = adj_matrix.nnz
        return adj_matrix

    def direct_sum(self, target_automaton):
        labels = set(self.edges.keys()).intersection(set(target_automaton.edges.keys()))
        direct_sum = dict()
        for label in labels:
            direct_sum[label] = dok_matrix(
                block_diag((target_automaton.edges[label], self.edges[label]))
            )
        return direct_sum

    def create_front(self, target_automaton, start_states_indices):
        front = dok_matrix(
            (
                target_automaton.number_of_states,
                self.number_of_states + target_automaton.number_of_states,
            ),
            dtype=bool,
        )
        self_start_row = dok_matrix((1, self.number_of_states), dtype=bool)
        for i in start_states_indices:
            self_start_row[0, i] = True
        for state_name in target_automaton.start_states:
            i = target_automaton.state_number[state_name]
            front[i, i] = True
            front[i, target_automaton.number_of_states :] = self_start_row
        return front

    def transform_front(self, target_automaton, front):
        transformed_front = dok_matrix(front.shape, dtype=bool)
        for i, j in zip(*front.nonzero()):
            if j < target_automaton.number_of_states:
                nnz_row_for_self_automaton = front[
                    i, target_automaton.number_of_states :
                ]
                if nnz_row_for_self_automaton.nnz > 0:
                    row_for_each_start = (
                        i
                        // target_automaton.number_of_states
                        * target_automaton.number_of_states
                    )
                    transformed_front[row_for_each_start + j, j] = True
                    transformed_front[
                        row_for_each_start + j, target_automaton.number_of_states :
                    ] += nnz_row_for_self_automaton
        return transformed_front

    def bfs(self, target_automaton, for_each_start=False):
        start_states_indices = [self.state_number[state] for state in self.start_states]
        front = (
            vstack(
                [self.create_front(target_automaton, {i}) for i in start_states_indices]
            )
            if for_each_start
            else self.create_front(target_automaton, start_states_indices)
        )
        direct_sum = self.direct_sum(target_automaton)
        visited = dok_matrix(front.shape, dtype=bool)
        while True:
            old_visited = visited.copy()
            for dir_sum_matrix in direct_sum.values():
                new_front = (
                    visited @ dir_sum_matrix
                    if front is None
                    else front @ dir_sum_matrix
                )
                visited += self.transform_front(target_automaton, new_front)
            front = None
            if visited.nnz == old_visited.nnz:
                break

        results = set()
        target_states_names = list(target_automaton.state_number.keys())
        self_states_names = list(self.state_number.keys())
        for i, j in zip(*visited.nonzero()):
            if (
                j >= target_automaton.number_of_states
                and target_states_names[i % target_automaton.number_of_states]
                in target_automaton.final_states
            ):
                self_state = j - target_automaton.number_of_states
                if self_states_names[self_state] in self.final_states:
                    if for_each_start:
                        results.add(
                            (
                                start_states_indices[
                                    i // target_automaton.number_of_states
                                ],
                                self_state,
                            )
                        )
                    else:
                        results.add(self_state)
        return results
