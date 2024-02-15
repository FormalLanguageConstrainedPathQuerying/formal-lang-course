import pytest
import os
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.parent
TESTS = ROOT / "tests"

def configure_python_path():
    python_path = os.getenv("PYTHONPATH")

    if python_path is None:
        os.environ["PYTHONPATH"] = str(ROOT)
    else:
        os.environ["PYTHONPATH"] += ";" + str(ROOT)

def run_tests():
    os.chdir(TESTS)

    pytest.main(["test_2.py"])

    os.chdir(ROOT)


if __name__ == "__main__":
    configure_python_path()
    run_tests()

