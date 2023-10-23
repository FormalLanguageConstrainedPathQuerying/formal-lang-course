from pathlib import Path

from pyformlang.cfg import CFG, Variable


def from_file(path: Path, start_non_terminal: str = None) -> CFG:
    if start_non_terminal is None:
        start_non_terminal = "S"
    with open(path, "r") as file:
        text_cfg = file.read()
    return CFG.from_text(text_cfg, Variable(start_non_terminal))
