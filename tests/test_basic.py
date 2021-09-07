import pytest
import project  # on import will print something from __init__ file


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_1():
    assert 1 + 1 == 2


def test_2():
    assert "1" + "1" == "11"
