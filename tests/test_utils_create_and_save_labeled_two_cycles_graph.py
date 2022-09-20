from project import *
import filecmp
import os.path

test_dir_path = os.path.dirname(os.path.abspath(__file__))


def test_42_13_formal_language():
    test_path = os.sep.join([test_dir_path, "test.dot"])
    exp_path = os.sep.join([test_dir_path, "expected.dot"])
    create_and_save_labeled_two_cycles_graph(42, 13, ("formal", "language"), test_path)
    assert filecmp.cmp(test_path, exp_path)
    os.remove(test_path)
