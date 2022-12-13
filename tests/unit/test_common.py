import unittest
from epos4 import Epos4Common


class TestCrc(unittest.TestCase):
    def setUp(self) -> None:
        self.common = Epos4Common()

    def test_parse_and_calc_crc(self):
        """
        Test parsing of list with data and calculating CRC
        """
        #     CRC    Data for calculating CRC (data from EPOS Studio 3.7)
        data = {
            0xE66C: [0x60, 0x02, 0x01, 0x61, 0x60, 0x00],  # Get Operation Mode
            0x6286: [0x60, 0x02, 0x01, 0x81, 0x60, 0x00],  # Get Position Profile
            0xD122: [0x60, 0x02, 0x01, 0x41, 0x60, 0x00],  # Get Fault State
            0x08A1: [0x68, 0x04, 0x01, 0x03, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00],  # Clear Fault
            0x4200: [0x68, 0x04, 0x01, 0x81, 0x60, 0x00, 0x10, 0x27, 0x00, 0x00],  # Set Position Profile
            0xFC70: [0x68, 0x04, 0x01, 0x10, 0x10, 0x01, 0x73, 0x61, 0x76, 0x65],  # Store
            0x6E6E: [0x68, 0x04, 0x01, 0x7A, 0x60, 0x00, 0xE8, 0x03, 0x00, 0x00],  # Move to position
        }
        for i in data:
            self.assertEqual(self.common.parse_and_calc_crc(data[i]), i)


        data = [
            [0x00, 0x02, 0x00, 0x00, 0x00, 0x00],
            [0x00, 0x02, 0x00, 0x00, 0x03, 0x05],
            [0x00, 0x02, 0x04, 0x00, 0x04, 0x05],
            [0x00, 0x02, 0x01, 0x00, 0x01, 0x06],
            [0x00, 0x02, 0x02, 0x00, 0x01, 0x06],
            [0x00, 0x02, 0x00, 0x00, 0x06, 0x06],
        ]
        for i in data:
            print(hex(self.common.parse_and_calc_crc(i)))


class TestByteSplitter(unittest.TestCase):
    def setUp(self) -> None:
        self.common = Epos4Common()

    def test_restuffing_data(self):
        data = {
            0: [
                [0x90, 0x02, 0x68, 0x04, 0x61, 0x60, 0x00, 0x90, 0x90, 0x90, 0x90, 0x70, 0xAA, 0x90, 0x90, 0x77],
                [0x90, 0x02, 0x68, 0x04, 0x61, 0x60, 0x00, 0x90, 0x90, 0x70, 0xAA, 0x90, 0x77]
            ],
            1: [
                [0x90, 0x02, 0x68, 0x04, 0x90, 0x90, 0x60, 0x00, 0xF0, 0x00, 0x70, 0xAA, 0x77, 0x90, 0x90],
                [0x90, 0x02, 0x68, 0x04, 0x90, 0x60, 0x00, 0xF0, 0x00, 0x70, 0xAA, 0x77, 0x90]
            ],
            2: [
                [0x90, 0x02, 0x68, 0x04, 0x90, 0x90, 0x60, 0x00, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0x90, 0xFF,
                 0xFF],
                [0x90, 0x02, 0x68, 0x04, 0x90, 0x60, 0x00, 0x90, 0x90, 0x90, 0x90, 0xFF, 0xFF]
            ],
        }
        for i in data:
            self.assertEqual(self.common.restuffing_data(data[i][0]), data[i][1])

    def test_high_byte(self):
        data = {
            0x45: 0x4566,
            0xAA: 0xAA12,
            0xFF: 0xFF8D,
            0xCA: 0xCAC3,
        }
        for i in data:
            self.assertEqual(self.common.high_byte(data[i]), i)

    def test_low_byte(self):
        data = {
            0x66: 0x4566,
            0x12: 0xAA12,
            0x8D: 0xFF8D,
            0xC3: 0xCAC3,
        }
        for i in data:
            self.assertEqual(self.common.low_byte(data[i]), i)

    def test_high_bytes_32(self):
        data = {
            0x4566: 0x4566FFAA,
            0xAA12: 0xAA12A3D1,
            0xFF8D: 0xFF8D3410,
            0xCAC3: 0xCAC3DAD4,
        }
        for i in data:
            self.assertEqual(self.common.high_bytes_32(data[i]), i)

    def test_low_bytes_32(self):
        data = {
            0xFFAA: 0x4566FFAA,
            0xA3D1: 0xAA12A3D1,
            0x3410: 0xFF8D3410,
            0xDAD4: 0xCAC3DAD4,
        }
        for i in data:
            self.assertEqual(self.common.low_bytes_32(data[i]), i)

    def test_restore_word(self):
        data = {
            0xFFAA: [0xFF, 0xAA],
            0xA3D1: [0xA3, 0xD1],
            0x3410: [0x34, 0x10],
            0xDAD4: [0xDA, 0xD4],
        }
        for i in data:
            self.assertEqual(self.common.restore_word(data[i][1], data[i][0]), i)


if __name__ == "__main__":
    unittest.main()
