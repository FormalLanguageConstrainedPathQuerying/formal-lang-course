from typing import Iterable

from pyformlang.cfg import Variable

from project.grammars.rsm_box import RSMBox

__all__ = ["RSM"]


class RSM:
    """
    Recursive State Machine

    Attributes
    ----------
    start_symbol: Variable
        RSM start symbol
    boxes: Iterable[RSMBox]
        RSM boxes
    """

    def __init__(
        self,
        start_symbol: Variable,
        boxes: Iterable[RSMBox],
    ):
        self._start_symbol = start_symbol
        self._boxes = boxes

    def set_start_symbol(self, start_symbol: Variable):
        """
        Set start_symbol

        Parameters
        ----------
        start_symbol: Variable
            RSM start_symbol
        """
        self._start_symbol = start_symbol

    def minimize(self):
        """
        Minimize each box in RSM

        Returns
        -------
        rsm: RSM
            RSM with minimized boxes
        """
        minimized_boxes = []
        for box in self.boxes:
            minimized_boxes.append(box.minimize())
        return RSM(start_symbol=self._start_symbol, boxes=minimized_boxes)

    @property
    def boxes(self):
        """
        Get boxes

        Returns
        -------
        boxes: Iterable[RSMBox]
            self._boxes field
        """
        return self._boxes

    @property
    def start_symbol(self):
        """
        Get start_symbol

        Returns
        -------
        start_symbol: Variable
            self._start_symbol field
        """
        return self._start_symbol
