import pytest
from pyformlang.cfg import CFG

from project.cfg import cyk
from tests.utils import read_data_from_json


@pytest.mark.parametrize(
    "cfg, word, expected",
    read_data_from_json(
        "test_cyk",
        lambda data: (CFG.from_text(data["cfg"]), data["word"], data["expected"]),
    ),
)
def test_cyk(cfg: CFG, word: str, expected: bool):
    assert cyk(cfg, word) == expected
