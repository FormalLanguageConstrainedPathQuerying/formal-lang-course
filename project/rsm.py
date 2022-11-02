from pyformlang.cfg import Variable


class RSM:
    def __init__(self, start_symbol: Variable, boxes: dict):
        self.start_symbol = start_symbol
        self.boxes = boxes
