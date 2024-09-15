import os

import pytest
import networkx as nx

from pathlib import Path
from project.regex_utils import regex_to_dfa


@pytest.mark.parametrize("regex", ["[ab]*c"])
def test_regex_to_dfa(regex: str):
    path = Path("tests/test_data/utils") / Path(regex + ".dot")
    dfa = regex_to_dfa(regex)
    nx.nx_pydot.write_dot(dfa.to_networkx(), path)

    # Comment if you want to see result DFA at the https://dreampuf.github.io/GraphvizOnline/
    os.remove(path)
