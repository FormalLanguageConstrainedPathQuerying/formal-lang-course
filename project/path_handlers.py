import os


def check_path(path: str) -> None:
    if not os.path.exists(path):
        raise OSError("Error: specified file does not exist.")
    if os.path.getsize(path) == 0:
        raise OSError("Error: specified file is empty.")
