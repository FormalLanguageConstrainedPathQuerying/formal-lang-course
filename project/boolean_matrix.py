class BooleanMatrix:
    def __init__(
        self, idx_states: dict, start_states: set, final_states: set, matrix: dict
    ):
        self.idx_states = idx_states
        self.start_states = start_states
        self.final_states = final_states
        self.matrix = matrix
