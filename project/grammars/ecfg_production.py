from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex

__all__ = ["ECFGProduction"]


class ECFGProduction:
    """
    ECFG Production class

    Attributes
    ----------
    head: Variable
        Production variable
    body: Regex
        Production body
    """

    def __init__(self, head: Variable, body: Regex):
        self._head = head
        self._body = body

    def __str__(self):
        return str(self._head) + " -> " + str(self._body)

    @property
    def head(self):
        """
        Get head

        Returns
        -------
        head: Variable
            self._head field
        """
        return self._head

    @property
    def body(self):
        """
        Get body

        Returns
        -------
        body: Regex
            self._body field
        """
        return self._body
