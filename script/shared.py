import os
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
TEST = ROOT / "test"
DOCS = ROOT / "docs"


def configure_python_path():
    python_path = os.getenv("PYTHONPATH")

    if python_path is None:
        os.environ["PYTHONPATH"] = str(ROOT)
    else:
        os.environ += str(ROOT)
    print("Configure python path: ", os.getenv("PYTHONPATH"))
