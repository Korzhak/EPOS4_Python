from . import definitions as df
from .common import Epos4Common
from .datatypes import (
    BYTE, WORD, DWORD
)


# TODO: check all descriptions of methods


class Epos4CommandMaker(Epos4Common):
    def __init__(self, node_id):
        super(Epos4CommandMaker, self).__init__()
        self._node_id = BYTE(node_id)
        self._DLE = BYTE(0x90)  # Data Link Escape
        self._STX = BYTE(0x02)  # Start of Text

    def _make_frame(self, op_code: int, number_of_words: int, data_list: list) -> bytes:
        # TODO: make description of method
        sync_bytes = [self._DLE.get(), self._STX.get()]
        intermediate_data = []
        final_data = []

        intermediate_data += [op_code, number_of_words]
        for bts in data_list:
            if type(bts) == WORD:
                intermediate_data.append(self.low_byte(bts.get()))
                intermediate_data.append(self.high_byte(bts.get()))
            elif type(bts) == DWORD:
                byte_0_1 = self.low_bytes_32(bts.get())
                byte_2_3 = self.high_bytes_32(bts.get())
                intermediate_data.append(self.low_byte(byte_0_1))
                intermediate_data.append(self.high_byte(byte_0_1))
                intermediate_data.append(self.low_byte(byte_2_3))
                intermediate_data.append(self.high_byte(byte_2_3))
            else:  # if BYTE type
                intermediate_data.append(bts.get())

        # Calc CRC
        crc = self.parse_and_calc_crc(intermediate_data)

        final_data += sync_bytes
        for byte in intermediate_data:
            final_data += self.stuffing_data(byte)

        final_data += self.stuffing_data(self.low_byte(crc))
        final_data += self.stuffing_data(self.high_byte(crc))
        frame = bytes(final_data)
        return frame

    # USER METHODS
    def set_node_id(self, node_id: int):
        self._node_id.set(node_id)

    def get_node_id(self) -> int:
        return self._node_id.get()

    def send_controlword(self, controlword: int) -> bytes:
        """
        Send controlword;
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_CONTROLWORD)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        cw = DWORD(controlword)
        data_list = [self._node_id, index, sub_index, cw]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def get_controlword(self) -> bytes:
        """
        TODO: write doc
        :return:
        """
        index = WORD(df.INDEX_CONTROLWORD)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def get_statusword(self) -> bytes:
        """
        Get statusword;
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_STATUSWORD)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    # Operation Mode
    def get_operation_mode(self) -> bytes:
        """
        Get target position
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_OM_GET_OPERATION_MODE)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def set_operation_mode(self, operation_mode: int) -> bytes:
        """
        Get target position
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_OM_SET_OPERATION_MODE)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        op_mode = DWORD(operation_mode)
        data_list = [self._node_id, index, sub_index, op_mode]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    # Profile Position Mode
    def get_position_profile_velocity(self) -> bytes:
        """
        Get PPM
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_PPM_PROFILE_VELOCITY)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def get_position_profile_acceleration(self) -> bytes:
        """
        Get PPM
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_PPM_PROFILE_ACCELERATION)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def get_position_profile_deceleration(self) -> bytes:
        """
        Get PPM
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_PPM_PROFILE_DECELERATION)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def set_position_profile_velocity(self, velocity: int) -> bytes:
        """
        Set PPM velocity
        :param velocity: int32 value
        :return: frame for sending to EPOS4
        """
        sub_index = BYTE(df.BLANK_SUBINDEX)
        index = WORD(df.INDEX_PPM_PROFILE_VELOCITY)
        vel = DWORD(velocity)
        data_list = [self._node_id, index, sub_index, vel]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def set_position_profile_acceleration(self, acceleration: int) -> bytes:
        """
        Set PPM acceleration
        :param acceleration: int32 value
        :return: frame for sending to EPOS4
        """
        sub_index = BYTE(df.BLANK_SUBINDEX)
        index = WORD(df.INDEX_PPM_PROFILE_ACCELERATION)
        acc = DWORD(acceleration)
        data_list = [self._node_id, index, sub_index, acc]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def set_position_profile_deceleration(self, deceleration: int) -> bytes:
        """
        Set PPM deceleration
        :param deceleration: int32 value
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_PPM_PROFILE_DECELERATION)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        dec = DWORD(deceleration)
        data_list = [self._node_id, index, sub_index, dec]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def get_target_position(self) -> bytes:
        """
        Get target position
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_PPM_PROFILE_POSITION)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data_list = [self._node_id, index, sub_index]
        return self._make_frame(df.READ_OPCODE, df.READ_OPCODE_NoW, data_list)

    def move_to_position(self, position: int) -> bytes:
        """
        Move to position
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_PPM_PROFILE_POSITION)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        pos = DWORD(position)
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

    def delete_error(self):
        """
        TODO: write doc
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_DELETE_ERROR)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data = DWORD(0)
        data_list = [self._node_id, index, sub_index, data]
        return self._make_frame(df.WRITE_OPCODE, df.WRITE_OPCODE_NoW, data_list)

    def clear_fault(self):
        """
        TODO: write doc
        :return: frame for sending to EPOS4
        """
        index = WORD(df.INDEX_CONTROLWORD)
        sub_index = BYTE(df.BLANK_SUBINDEX)
        data = DWORD(df.CW_CLEAR_FAULT)
        data_list = [self._node_id, index, sub_index, data]
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
