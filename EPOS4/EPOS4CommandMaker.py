from EPOS4 import Definitions as df
from EPOS4 import datatypes as dt

# TODO: check all descriptions of methods


class EPOS4CommandMaker:
    def __init__(self, node_id):
        self._node_id = dt.BYTE(node_id)
        self._DLE = 0x90  # Data Link Escape
        self._STX = 0x02  # Start of Text
        self._frame = b''

    @staticmethod
    def _low_byte(bts) -> int:
        """
        Separate two bytes of int 16 value;
        :param bts: int16
        :return: LSB int8
        """
        return bts & 0xFF

    @staticmethod
    def _high_byte(bts) -> int:
        """
        Separate two bytes of int 16 value;
        :param bts: int16
        :return: MSB int8
        """
        return (bts >> 8) & 0xFF

    @staticmethod
    def _low_bytes_32(bts) -> int:
        """
        Separate four bytes of int 32 value;
        :param bts: int32
        :return: LSB int16
        """
        return bts & 0xFFFF

    @staticmethod
    def _high_bytes_32(bts) -> int:
        """
        Separate four bytes of int 32 value;
        :param bts: int32
        :return: MSB int16
        """
        return (bts >> 16) & 0xFFFF

    @staticmethod
    def _restore_word(low_byte, high_byte) -> int:
        """
        Reverse process to _low_byte and _high_byte;
        :param low_byte: returned value _low_byte()
        :param high_byte: returned value _high_byte()
        :return: Restored value of 2 bytes
        """
        return (high_byte << 8) | low_byte

    @staticmethod
    def _calc_crc(data_for_calc: list) -> int:
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

    @staticmethod
    def _stuffing_data(byte: int) -> list:
        if byte == 0x90:
            return [0x90, 0x90]
        return [byte]

    def _parse_and_calc_crc(self, data: list) -> int:
        """
        Parse command frame to calculate CRC
        :param data: command frame
        :return: CRC
        """
        item = 0
        data_for_calc = []
        while item < len(data):
            data_for_calc.append(self._restore_word(data[item], data[item+1]))
            item += 2

        data_for_calc.append(0x0000)  # last byte for CRC
        return self._calc_crc(data_for_calc)

    def _make_frame(self, op_code: int, number_of_words: int, data_list: list,) -> bytearray:
        sync_bytes = [self._DLE, self._STX]
        intermediate_data = []
        final_data = []

        # full_header_u16 = self._restore_word(op_code, number_of_words)
        # data_for_crc = [full_header_u16] + [item.get() for item in data_list] + [0x0000]
        # crc = self._calc_crc(data_for_crc)

        # final_data = sync_bytes_int8 + self._stuffing_data(op_code) + self._stuffing_data(number_of_words)
        #
        # for bts in data_list:
        #     if type(bts) == dt.WORD:
        #         final_data += self._stuffing_data(self._low_byte(bts.get()))
        #         final_data += self._stuffing_data(self._high_byte(bts.get()))
        #     elif type(bts) == dt.DWORD:
        #         byte_0_1 = self._low_bytes_32(bts.get())
        #         byte_2_3 = self._high_bytes_32(bts.get())
        #         final_data += self._stuffing_data(self._low_byte(byte_0_1))
        #         final_data += self._stuffing_data(self._high_byte(byte_0_1))
        #         final_data += self._stuffing_data(self._low_byte(byte_2_3))
        #         final_data += self._stuffing_data(self._high_byte(byte_2_3))
        #     else:  # if dt.BYTE type
        #         final_data += self._stuffing_data(bts.get())

        intermediate_data += [op_code, number_of_words]
        for bts in data_list:
            if type(bts) == dt.WORD:
                intermediate_data.append(self._low_byte(bts.get()))
                intermediate_data.append(self._high_byte(bts.get()))
            elif type(bts) == dt.DWORD:
                byte_0_1 = self._low_bytes_32(bts.get())
                byte_2_3 = self._high_bytes_32(bts.get())
                intermediate_data.append(self._low_byte(byte_0_1))
                intermediate_data.append(self._high_byte(byte_0_1))
                intermediate_data.append(self._low_byte(byte_2_3))
                intermediate_data.append(self._high_byte(byte_2_3))
            else:  # if dt.BYTE type
                intermediate_data.append(bts.get())

        # Calc CRC
        crc = self._parse_and_calc_crc(intermediate_data)

        final_data += sync_bytes
        for byte in intermediate_data:
            final_data += self._stuffing_data(byte)

        final_data += self._stuffing_data(self._low_byte(crc))
        final_data += self._stuffing_data(self._high_byte(crc))
        self._frame = bytearray(final_data)
        return self._frame
        # return final_data

    # USER METHODS
    def set_node_id(self, node_id: int):
        self._node_id.set(node_id)

    def get_node_id(self) -> int:
        return self._node_id.get()

    def send_controlword(self, controlword: int):
        """
        Send controlword;
        :return: frame for sending to EPOS4
        """
        index = dt.WORD(df.INDEX_OM_SET_OPERATION_MODE)
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        cw = dt.DWORD(controlword)
        data_list = [self._node_id, index, sub_index, cw]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    # Operation Mode
    def get_operation_mode(self) -> bytearray:
        """
        Get target position
        :return: frame for sending to EPOS4
        """
        index = dt.WORD(df.INDEX_OM_GET_OPERATION_MODE)
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def set_operation_mode(self, operation_mode: int) -> bytearray:
        """
        Get target position
        :return: frame for sending to EPOS4
        """
        index = dt.WORD(df.INDEX_OM_SET_OPERATION_MODE)
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        op_mode = dt.DWORD(operation_mode)
        data_list = [self._node_id, index, sub_index, op_mode]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    # Profile Position Mode
    def get_position_profile(self) -> bytearray:
        """
        Get PPM
        :return: frame for sending to EPOS4
        """
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        index = dt.WORD(df.INDEX_PPM_PROFILE_VELOCITY)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def set_position_profile_velocity(self, velocity: int) -> bytearray:
        """
        Set PPM velocity
        :param velocity: int32 value
        :return: frame for sending to EPOS4
        """
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        index = dt.WORD(df.INDEX_PPM_PROFILE_VELOCITY)
        vel = dt.DWORD(velocity)
        data_list = [self._node_id, index, sub_index, vel]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def set_position_profile_acceleration(self, acceleration: int) -> bytearray:
        """
        Set PPM acceleration
        :param acceleration: int32 value
        :return: frame for sending to EPOS4
        """
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        index = dt.WORD(df.INDEX_PPM_PROFILE_ACCELERATION)
        acc = dt.DWORD(acceleration)
        data_list = [self._node_id, index, sub_index, acc]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def set_position_profile_deceleration(self, deceleration: int) -> bytearray:
        """
        Set PPM deceleration
        :param deceleration: int32 value
        :return: frame for sending to EPOS4
        """
        index = dt.WORD(df.INDEX_PPM_PROFILE_DECELERATION)
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        dec = dt.DWORD(deceleration)
        data_list = [self._node_id, index, sub_index, dec]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def get_target_position(self) -> bytearray:
        """
        Get target position
        :return: frame for sending to EPOS4
        """
        index = dt.WORD(df.INDEX_PPM_PROFILE_POSITION)
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def move_to_position(self, position: int) -> bytearray:
        """
        Move to position
        :return: frame for sending to EPOS4
        """
        index = dt.WORD(df.INDEX_PPM_PROFILE_POSITION)
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        pos = dt.DWORD(position)
        data_list = [self._node_id, index, sub_index, pos]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def halt_position_movement(self):
        pass

    # Motion Info
    def get_movement_state(self):
        pass

    def get_current_is(self):
        pass

    def get_position_is(self):
        pass

    # State Machine
    def get_fault_state(self):
        pass

    def clear_fault(self):
        pass

    def set_enable_state(self):
        """
                Send controlword;
                :return: frame for sending to EPOS4
                """
        index = dt.WORD(df.INDEX_CONTROLWORD)
        sub_index = dt.BYTE(df.BLANK_SUBINDEX)
        cw = dt.DWORD(0x06)
        data_list = [self._node_id, index, sub_index, cw]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def set_disable_state(self):
        pass

    # Error Handling
    def reset_device(self):
        pass

    def clear_device_errors(self):
        pass

    def get_device_error_code(self):
        pass
