from scipy import sparse

from project.utils.boolean_matrix import BooleanMatrix

__all__ = ["RSMMatrixSparse"]


class RSMMatrixSparse(BooleanMatrix):
    """
    Representation of RSM as a Boolean Matrix
    Using scipy.sparse dok_matrix implementation
    """

    def __init__(self):
        super().__init__()

    def get_transitive_closure(self):
        if self.bmatrix.values():
            tc = sum(self.bmatrix.values())
        else:
            return self._create_bool_matrix(
                (self.number_of_states, self.number_of_states)
            )

        prev_nnz = tc.nnz
        new_nnz = 0

        while prev_nnz != new_nnz:
            tc += tc @ tc
            prev_nnz, new_nnz = new_nnz, tc.nnz

        return tc

    @staticmethod
    def _kron(bm1, bm2):
        return sparse.kron(bm1, bm2, format="dok")

    @staticmethod
    def _create_bool_matrix(shape):
        return sparse.dok_matrix(shape, dtype=bool)

    @staticmethod
    def _get_nonzero(bm):
        return zip(*bm.nonzero())
