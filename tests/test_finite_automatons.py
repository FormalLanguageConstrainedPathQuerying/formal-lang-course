import project.hw02 as fa
import pytest
from tempfile import NamedTemporaryFile
from textwrap import dedent


@pytest.mark.parametrize("regex_str",
                         ['abc def',
                          'abc|def',
                          'abc def | def abc',
                          'abc def*',
                          'abc* def',
                          '(abc* def*)*'])
def test_regex_dfa_minimal(regex_str: str):
    dfa = fa.make_regex_dfa(regex_str)
    assert dfa.is_deterministic()
    minimal = dfa.minimize()
    assert dfa.is_equivalent_to(minimal)
    assert len(minimal.states) == len(dfa.states)
    assert minimal.get_number_transitions() == dfa.get_number_transitions()


def test_regex_dfa():
    dfa = fa.make_regex_dfa('abc (abc* def*)*')
    path = ""
    with NamedTemporaryFile(delete=False) as f:
        path = f.name
    dfa.write_as_dot(path)
    with open(path) as f:
        contents = "".join(f.readlines())
    expected = """\
        digraph  {
        "1;10;11;4;5;6;7;8;1;10;2;3;4;5;6;7;8;1;10;4;5;6;7;8;9" [is_final=True, is_start=False, label="1;10;11;4;5;6;7;8;1;10;2;3;4;5;6;7;8;1;10;4;5;6;7;8;9", peripheries=2];
        0 [is_final=False, is_start=True, label=0, peripheries=1];
        "0_starting" [height="0.0", label="", shape=None, width="0.0"];
        "1;10;11;4;5;6;7;8;1;10;2;3;4;5;6;7;8;1;10;4;5;6;7;8;9" -> "1;10;11;4;5;6;7;8;1;10;2;3;4;5;6;7;8;1;10;4;5;6;7;8;9"  [key=0, label=def];
        "1;10;11;4;5;6;7;8;1;10;2;3;4;5;6;7;8;1;10;4;5;6;7;8;9" -> "1;10;11;4;5;6;7;8;1;10;2;3;4;5;6;7;8;1;10;4;5;6;7;8;9"  [key=1, label=abc];
        0 -> "1;10;11;4;5;6;7;8;1;10;2;3;4;5;6;7;8;1;10;4;5;6;7;8;9"  [key=0, label=abc];
        "0_starting" -> 0  [key=0];
        }
        """
    expected = dedent(expected)
    contents = dedent(contents)
    assert expected == contents
