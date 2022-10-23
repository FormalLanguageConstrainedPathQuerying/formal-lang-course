from functools import reduce
from os import listdir
from os.path import isfile

import pytest
from pyformlang.cfg import CFG, Terminal, Variable

from project.cfg_utils import import_cfg_from_file, from_cfg_to_weak_cnf

path_to_tests = "./resources/test_from_cfg_to_weak_cnf/"
max_word_len = 10

testdata = [
    path_to_tests + f for f in listdir(path_to_tests) if isfile(path_to_tests + f)
]


def check_cfg_in_weak_cnf(cfg: CFG) -> bool:
    try:
        for production in cfg.productions:
            match len(production.body):
                case 0:
                    assert True  # epsilon body
                case 1:
                    assert isinstance(production.body[0], Terminal)
                case 2:
                    assert isinstance(production.body[0], Variable) and isinstance(
                        production.body[1], Variable
                    )
                case _:
                    assert False
    except AssertionError:
        return False

    return True


@pytest.mark.parametrize("path_to_actual", testdata)
def test_from_cfg_to_weak_cnf(path_to_actual: str):
    cfg = import_cfg_from_file(path_to_actual)
    weak_cnf_cfg = from_cfg_to_weak_cnf(cfg)

    # in tests we dont use wide words but there are infinite grammars
    expected_words = set()
    for word in cfg.get_words(max_length=max_word_len):
        expected_words.add(reduce(lambda acc, symbol: acc + str(symbol), word, ""))
    actual_words = set()
    for word in weak_cnf_cfg.get_words(max_length=max_word_len):
        actual_words.add(reduce(lambda acc, symbol: acc + str(symbol), word, ""))

    assert check_cfg_in_weak_cnf(weak_cnf_cfg) and expected_words == actual_words
