import os
import pathlib
import platform

ROOT = pathlib.Path(__file__).parent.parent
DOCS = ROOT / "docs"
TESTS = ROOT / "tests"
PYTHON_INTERPRETER = (
    "python" if platform.system() != "Windows" else ROOT / "venv/Scripts/python.exe"
)


def configure_python_path():
    python_path = os.getenv("PYTHONPATH")

    if python_path is None:
        os.environ["PYTHONPATH"] = str(ROOT)
    else:
        os.environ["PYTHONPATH"] += ";" + str(ROOT)
    print("Configure python path: ", os.getenv("PYTHONPATH"))
