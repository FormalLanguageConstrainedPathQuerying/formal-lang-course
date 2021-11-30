import pycubool as cb

from project.utils.boolean_matrix import BooleanMatrix

__all__ = ["RSMMatrixCB"]


class RSMMatrixCB(BooleanMatrix):
    """
    Representation of RSM as a Boolean Matrix
    Using pycubool sparse matrix implementation (GPU-supported)
    """

    def __init__(self):
        super().__init__()

    def get_transitive_closure(self):
        tc = cb.Matrix.empty(shape=(self.number_of_states, self.number_of_states))
        for bm in self.bmatrix.values():
            tc.ewiseadd(bm, out=tc)
        prev_nnz = tc.nvals
        new_nnz = 0

        while prev_nnz != new_nnz:
            tc.mxm(tc, out=tc, accumulate=True)
            prev_nnz, new_nnz = new_nnz, tc.nvals

        return tc

    @staticmethod
    def _kron(bm1, bm2):
        return bm1.kronecker(bm2)

    @staticmethod
    def _create_bool_matrix(shape):
        return cb.Matrix.empty(shape)

    @staticmethod
    def _get_nonzero(bm):
        return zip(*bm.to_lists())
