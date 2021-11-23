from scipy.sparse import dok_matrix


class BooleanMatrix:
    """
    Boolean Matrix base class

    Attributes
    ----------
    bmatrix: dict
        Dictionary of boolean matrices.
        Keys are NFA labels
    block_size: int
        Size of a block in boolean matrix
    """

    def __init__(self):
        self.bmatrix = dict()
        self.block_size = 1

    def transitive_closure(self):
        """
        Computes transitive closure of boolean matrices

        Returns
        -------
        tc: dok_matrix
            Transitive closure of boolean matrices
        """
        if not self.bmatrix.values():
            return dok_matrix((1, 1))

        tc = sum(self.bmatrix.values())

        prev_nnz = tc.nnz
        curr_nnz = 0

        while prev_nnz != curr_nnz:
            tc += tc @ tc
            prev_nnz, curr_nnz = curr_nnz, tc.nnz

        return tc
