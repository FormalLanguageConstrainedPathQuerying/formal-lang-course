import unittest


class BasicTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        assert 1 + 1 == 2

    def test_2(self):
        assert "1" + "1" == "11"
