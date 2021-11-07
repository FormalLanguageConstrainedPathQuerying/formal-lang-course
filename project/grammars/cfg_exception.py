__all__ = ["CFGException"]


class CFGException(Exception):
    """
    Base exception for operations with CFG and ECFG
    """

    def __init__(self, msg):
        self.msg = msg
