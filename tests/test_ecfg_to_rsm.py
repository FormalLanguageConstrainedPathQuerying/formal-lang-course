import pytest

from project.grammars.rsm_box import RSMBox
from project.grammars.ecfg import ECFG
from project.utils.CFG_utils import transform_ecfg_to_rsm, transform_regex_to_dfa


@pytest.mark.parametrize(
    """ecfg_text""",
    (
        """
        """,
        """
        S -> $
        """,
        """
        S -> (a S b S) f*
        B -> B | (B C)
        C -> A B C
        """,
    ),
)
def test_boxes_regex_equality(ecfg_text):
    ecfg = ECFG.from_text(ecfg_text)
    rsm = transform_ecfg_to_rsm(ecfg)
    act_start_symbol = ecfg.start_symbol
    exp_start_symbol = rsm.start_symbol
    exp_boxes = [
        RSMBox(p.head, transform_regex_to_dfa(str(p.body))) for p in ecfg.productions
    ]
    act_boxes = rsm.boxes
    return act_start_symbol == exp_start_symbol and act_boxes == exp_boxes
