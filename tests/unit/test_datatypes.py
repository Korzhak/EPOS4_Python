import unittest
from src.epos4.datatypes import BYTE, WORD, DWORD, ListOfBytes

# TODO: write unit tests for datatypes


class TestByte(unittest.TestCase):
    def setUp(self) -> None:
        self.byte = BYTE()

    def test_set(self):
        pass

    def test_set_from_reversed_bytes(self):
        pass

    def test_eq(self):
        pass

    def test_ge(self):
        pass

    def test_gt(self):
        pass

    def test_le(self):
        pass

    def test_lt(self):
        pass

    def test_ne(self):
        pass

    def test_rshift(self):
        pass

    def test_rrshift(self):
        pass

    def test_lshift(self):
        pass

    def test_rlshift(self):
        pass

    def test_or(self):
        pass

    def test_ror(self):
        pass

    def test_xor(self):
        pass

    def test_rxor(self):
        pass

    def test_invert(self):
        pass


if __name__ == "__main__":
    unittest.main()
