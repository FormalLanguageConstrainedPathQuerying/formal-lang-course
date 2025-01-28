import numpy as np


def create_bool_vector(vector_size, true_indexes):
    vector = np.zeros(vector_size, dtype=bool)

    for true_ind in true_indexes:
        vector[true_ind] = True

    return vector
