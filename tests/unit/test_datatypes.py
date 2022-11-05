import unittest
from src.epos4.datatypes import BYTE, WORD, DWORD, ListOfBytes

# TODO: write unit tests for datatypes


class TestByte(unittest.TestCase):
    def setUp(self) -> None:
        self.byte = BYTE()

    def test_set(self):
        data = {
            0x55: 0x443655,
            0xCA: 0x1355CA,
            0x8D: 0xACCF8D,
            0xFF: 0x12345678CCAAFF,
            0xB1: 0x65438295789885B1
        }
        for i in data:
            b = BYTE()
            b.set(data[i])
            self.assertEqual(b.get(), i)

    def test_eq(self):
        data = [
            [BYTE(0), BYTE(0)],
            [BYTE(0xFF), BYTE(0xFF)],
            [BYTE(0xAB), BYTE(0xAB)],
            [BYTE(0xD1), BYTE(0xD1)],
            [BYTE(0x49), BYTE(0x49)],
            [BYTE(0xC5), BYTE(0xC5)],
            [BYTE(0x01), BYTE(0x01)],
        ]
        for i in data:
            self.assertEqual(i[0], i[1])

    def test_ge_lt(self):
        data = [
            [BYTE(0), BYTE(0)],
            [BYTE(0xFF), BYTE(0xFA)],
            [BYTE(0xAB), BYTE(0xAB)],
            [BYTE(0xD2), BYTE(0xD1)],
            [BYTE(0x4A), BYTE(0x49)],
            [BYTE(0xC5), BYTE(0xC5)],
            [BYTE(0x11), BYTE(0x01)],
        ]
        for i in data:
            self.assertTrue(i[0] >= i[1])

        for i in data:
            self.assertFalse(i[0] < i[1])

    def test_le_gt(self):
        data = [
            [BYTE(1), BYTE(1)],
            [BYTE(0xF9), BYTE(0xFA)],
            [BYTE(0xAB), BYTE(0xAB)],
            [BYTE(0xD0), BYTE(0xD1)],
            [BYTE(0x00), BYTE(0x49)],
            [BYTE(0xC5), BYTE(0xC5)],
            [BYTE(0x00), BYTE(0x01)],
        ]
        for i in data:
            self.assertTrue(i[0] <= i[1])

        for i in data:
            self.assertFalse(i[0] > i[1])

    def test_ne(self):
        data = [
            [BYTE(2), BYTE(1)],
            [BYTE(0xF9), BYTE(0xFA)],
            [BYTE(0xAF), BYTE(0xAB)],
            [BYTE(0xD0), BYTE(0xD1)],
            [BYTE(0x00), BYTE(0x49)],
            [BYTE(0xC9), BYTE(0xC5)],
            [BYTE(0x00), BYTE(0x01)],
        ]
        for i in data:
            self.assertNotEqual(i[0], i[1])

    def test_rshift(self):
        # TODO: write this test
        data = [
            [BYTE(2), BYTE(1)],
            [BYTE(0xF9), BYTE(0xFA)],
            [BYTE(0xAF), BYTE(0xAB)],
            [BYTE(0xD0), BYTE(0xD1)],
            [BYTE(0x00), BYTE(0x49)],
            [BYTE(0xC9), BYTE(0xC5)],
            [BYTE(0x00), BYTE(0x01)],
        ]
        self.assertEquals()

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
