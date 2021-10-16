import pytest

from project.grammar_tools import get_cnf_from_file


def test_wrong_file():
    path_not_exists = "tests/data/cfgs/emp"
    path_not_txt = "tests/data/cfgs/empty"
    path_to_empty = "tests/data/cfgs/empty.txt"

    with pytest.raises(OSError):
        get_cnf_from_file(path_not_exists)
    with pytest.raises(OSError):
        get_cnf_from_file(path_not_txt)
    with pytest.raises(OSError):
        get_cnf_from_file(path_to_empty)


def test_wrong_text():
    with pytest.raises(ValueError):
        get_cnf_from_file("tests/data/cfgs/wrong.txt")


@pytest.mark.parametrize(
    "filename, axiom",
    [("epsilon.txt", "epsilon"), ("from_lesson.txt", "S"), ("random.txt", "NP")],
)
def test_get_cnf_from_file(filename, axiom):
    path = "tests/data/cfgs/" + filename

    cnf = get_cnf_from_file(path, axiom)

    # It means Weak Chomsky Normal Form too
    assert cnf.is_normal_form()
