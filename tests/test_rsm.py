import pytest

from project.grammars.ecfg import ECFG
from project.utils.CFG_utils import transform_ecfg_to_rsm


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
        C -> (A* B*) | (A* B*)
        """,
    ),
)
def test_rsm_minimize(ecfg_text):
    ecfg = ECFG.from_text(ecfg_text)
    rsm = transform_ecfg_to_rsm(ecfg).minimize()
    rsm_box_automatas = [box.dfa for box in rsm.boxes]
    assert all(map(lambda x: x.is_equivalent_to(x.minimize()), rsm_box_automatas))
