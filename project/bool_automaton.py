from pyformlang.finite_automaton import FiniteAutomaton
from scipy.sparse import dok_matrix, kron


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
