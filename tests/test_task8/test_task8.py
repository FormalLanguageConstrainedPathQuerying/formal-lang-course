import pytest
from pyformlang.cfg import CFG

from project import cyk
from tests.utils import get_data


@pytest.mark.parametrize(
    "cfg, word, expected",
    get_data(
        "test_cyk",
        lambda d: (CFG.from_text(d["cfg"]), d["word"], d["expected"]),
    ),
)
def test_accepts(cfg: CFG, word: str, expected: bool):
    actual = cyk.cyk(cfg, word)
    assert actual == expected
