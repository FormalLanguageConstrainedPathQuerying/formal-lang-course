import pytest
import os

def run_tests():
    cur_path = os.getcwd()
    os.chdir("../../tests/")

    pytest.main(["test_basic.py"])

    os.chdir(cur_path)

if __name__ == "__main__":
    run_tests()

