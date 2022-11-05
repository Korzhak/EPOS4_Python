
class Epos4Common:
    def __init__(self):
        pass

    @staticmethod
    def low_byte(bts: int) -> int:
        """
        Separate two bytes of int 16 value;
        :param bts: int16
        :return: LSB int8
        """
        return bts & 0xFF

    @staticmethod
    def high_byte(bts: int) -> int:
        """
        Separate two bytes of int 16 value;
        :param bts: int16
        :return: MSB int8
        """
        return (bts >> 8) & 0xFF

    @staticmethod
    def low_bytes_32(bts: int) -> int:
        """
        Separate four bytes of int 32 value;
        :param bts: int32
        :return: LSB int16
        """
        return bts & 0xFFFF

    @staticmethod
    def high_bytes_32(bts: int) -> int:
        """
        Separate four bytes of int 32 value;
        :param bts: int32
        :return: MSB int16
        """
        return (bts >> 16) & 0xFFFF

    @staticmethod
    def restore_word(low_byte: int, high_byte: int) -> int:
        """
        Reverse process to _low_byte and _high_byte;
        :param low_byte: returned value _low_byte()
        :param high_byte: returned value _high_byte()
        :return: Restored value of 2 bytes
        """
        return (high_byte << 8) | low_byte

    @staticmethod
    def stuffing_data(byte: int) -> list:
        if byte == 0x90:
            return [0x90, 0x90]
        return [byte]

    @staticmethod
    def calc_crc(data_for_calc: list) -> int:
        """
        The 16-bit CRC checksum uses the algorithm CRC-CCITT.
        For calculation, the 16-bit generator polynomial “x16+x12+x5+x0” is used.
        The CRC is calculated before data stuffing and synchronization.
        Add a CRC value of “0” (zero) for CRC calculation.
        The data frame bytes must be calculated as a word;
        :param data_for_calc: array of uint16 bytes with data + last one element is 0 for CRC calc.
        :return: CRC in HEX format
        """
        crc = 0
        for i in range(len(data_for_calc)):
            shifter = 0x8000
            _c = data_for_calc[i]
            while shifter:
                carry = crc & 0x8000
                crc = (crc << 1) & 0xFFFF
                if _c & shifter:
                    crc += 1
                if carry:
                    crc ^= 0x1021
                shifter >>= 1

        return crc

    def parse_and_calc_crc(self, data: list) -> int:
        """
        Parse command frame to calculate CRC
        :param data: command frame
        :return: CRC
        """
        item = 0
        data_for_calc = []
        while item < len(data):
            data_for_calc.append(self.restore_word(data[item], data[item + 1]))
            item += 2

        data_for_calc.append(0x0000)  # last byte for CRC
        return self.calc_crc(data_for_calc)
