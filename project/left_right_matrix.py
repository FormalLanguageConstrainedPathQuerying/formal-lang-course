from scipy.sparse import spmatrix, vstack, coo_matrix


class LeftRightMatrix:
    """
    Class representing matrix which was constructed as concatenation of two matrix. These class must be used only inside
    regular_bfs() function.
    """

    def __init__(self, left_submatrix: spmatrix, right_submatrix: spmatrix):
        """
        :param left_submatrix: matrix which will be accessible as left_submatrix()
        :param right_submatrix: matrix which will be accessible as rigt_submatrix(). Height of right_submatrix must be
            same with left_submatrix
        """
        height_left, _ = left_submatrix.get_shape()
        height_right, _ = right_submatrix.get_shape()
        assert height_right == height_left
        self._left_submatrix = left_submatrix
        self._right_submatrix = right_submatrix

    def __copy__(self):
        return LeftRightMatrix(
            self._left_submatrix.copy(), self._right_submatrix.copy()
        )

    def __eq__(self, other):
        if not isinstance(other, LeftRightMatrix):
            return False
        nonzero_self = set(zip(*self._left_submatrix.nonzero())).union(
            set(zip(*self._right_submatrix.nonzero()))
        )
        nonzero_other = set(zip(*other._left_submatrix.nonzero())).union(
            set(zip(*other._right_submatrix.nonzero()))
        )
        return nonzero_self == nonzero_other

    def left_submatrix(self) -> spmatrix:
        return self._left_submatrix

    def right_submatrix(self) -> spmatrix:
        return self._right_submatrix

    _convert_to_spmatrix = lambda mat: mat.tocsr()

    def tospmatrix(self):
        _, width_left = self._left_submatrix.get_shape()
        height_right, width_right = self._right_submatrix.get_shape()
        left_submatrix = self._left_submatrix.tocsr()
        right_submatrix = self._right_submatrix.tocsr()
        data = [left_submatrix[i, j] for (i, j) in zip(*left_submatrix.nonzero())] + [
            right_submatrix[i, j] for (i, j) in zip(*right_submatrix.nonzero())
        ]
        row = [i for (i, _) in zip(*left_submatrix.nonzero())] + [
            i for (i, _) in zip(*right_submatrix.nonzero())
        ]
        col = [j for (_, j) in zip(*left_submatrix.nonzero())] + [
            width_left + j for (_, j) in zip(*right_submatrix.nonzero())
        ]
        return LeftRightMatrix._convert_to_spmatrix(
            coo_matrix(
                (data, (row, col)), shape=(height_right, width_right + width_left)
            )
        )

    def exclude_visited(self, visited: "LeftRightMatrix"):
        assert (
            self._left_submatrix.get_shape() == visited.left_submatrix().get_shape()
            and self._right_submatrix.get_shape()
            == visited.right_submatrix().get_shape()
        )
        visited_right_submatrix = visited.right_submatrix()
        for (i, j) in zip(*self._right_submatrix.nonzero()):
            if visited_right_submatrix[i, j] != 0:
                self._right_submatrix[i, j] = 0

    def merge(self, other: "LeftRightMatrix", merge_factor: int):
        assert (
            self._left_submatrix.get_shape() == other.left_submatrix().get_shape()
            and self._right_submatrix.get_shape() == other.right_submatrix().get_shape()
        )
        _, width_left = self._left_submatrix.get_shape()
        _, width_right = self._right_submatrix.get_shape()
        for (i, j) in zip(*other.left_submatrix().nonzero()):
            offset = i // merge_factor
            row = other.right_submatrix().getrow(i)
            for (_, k) in zip(*row.nonzero()):
                if row[0, k] != 0:
                    self._right_submatrix[offset * merge_factor + j, k] = 1

    @classmethod
    def vstack(
        cls, matrix1: "LeftRightMatrix", matrix2: "LeftRightMatrix"
    ) -> "LeftRightMatrix":
        return LeftRightMatrix(
            vstack((matrix1.left_submatrix(), matrix2.left_submatrix())).tolil(),
            vstack((matrix1.right_submatrix(), matrix2.right_submatrix())).tolil(),
        )
