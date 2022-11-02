from project.rsm import RSM
from project.ecfg import ECFG


class RSMManager:
    @staticmethod
    def minimize(rsm: RSM) -> RSM:
        boxes = {}
        for key, fa in rsm.boxes.items():
            boxes[key] = fa.minimize()

        return RSM(start_symbol=rsm.start_symbol, boxes=boxes)

    @staticmethod
    def create_rsm_from_ecfg(ecfg: ECFG) -> RSM:
        boxes = {}
        for (var, regex) in ecfg.productions.items():
            boxes[var] = regex.to_epsilon_nfa()

        return RSM(start_symbol=ecfg.start_symbol, boxes=boxes)
