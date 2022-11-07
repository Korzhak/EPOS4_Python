import serial
from . import statuses as ss
from . import datatypes as dt
from . import definitions as df
from .common import Epos4Common
from .command_maker import Epos4CommandMaker
from .feedback_parser import Epos4FeedbackParser


class Epos4:
    def __init__(self, com, baud_rate=115200, node_id=1):
        self.ser = serial.Serial(com, baud_rate)
        self._command_maker = Epos4CommandMaker(node_id)
        self._feedback_parser = Epos4FeedbackParser()

    def _wait_feedback(self, executed_opcode) -> dt.STATUS:
        """
        TODO: write description
        :param executed_opcode:
        :return:
        """
        first_time = True
        resp = dt.STATUS(ss.ERROR)
        header = b''
        status = dt.STATUS()
        # TODO: change for..range
        for i in range(2000):
            b = self.ser.inWaiting()
            if b:
                if first_time:
                    header = self.ser.read(4)
                    status = self._feedback_parser.parse_header(header)
                    first_time = False
                else:
                    number_of_words = status.get_returned_data()[3].get()
                    # NoW - count of int16 values, but we received int8, so NoW must be multiplied by 2.
                    # And +2 it is CRC bytes
                    frame = self.ser.read(number_of_words*2+2)
                    resp = self._feedback_parser.read_obj_response(number_of_words, executed_opcode, header, frame)
                    first_time = True
        return resp

    # Controlword and statusword methods
    def get_statusword(self) -> dt.STATUS:
        cmd = self._command_maker.get_statusword()
        status = dt.STATUS()
        while not status.get_is_crc_ok():
            self.ser.write(cmd)
            status = self._wait_feedback(df.READ_OPCODE)
        return status

    def get_controlword(self) -> dt.STATUS:
        cmd = self._command_maker.get_controlword()
        status = dt.STATUS()
        while not status.get_is_crc_ok():
            self.ser.write(cmd)
            status = self._wait_feedback(df.READ_OPCODE)
        return status

    # Operation mode methods
    def get_operation_mode(self) -> dt.BYTE:
        cmd = self._command_maker.get_operation_mode()
        status = dt.STATUS()
        while not status.get_is_crc_ok():
            self.ser.write(cmd)
            status = self._wait_feedback(df.READ_OPCODE)
        return status.get_returned_data()[-1]

    def set_operation_mode(self, op_mode: int) -> dt.STATUS:
        cmd = self._command_maker.set_operation_mode(op_mode)
        status = dt.STATUS()
        while not status.get_is_crc_ok():
            self.ser.write(cmd)
            status = self._wait_feedback(df.WRITE_OPCODE)
        return status

    # PPM methods
    def get_position_profile(self):
        pass

    def set_position_profile(self):
        pass

    def get_target_position(self):
        pass

    def move_to_position(self, position: int) -> dt.ListOfStatuses:
        list_of_statuses = dt.ListOfStatuses()

        # Set position
        status = dt.STATUS(ss.OK)
        cmd = self._command_maker.move_to_position(position)
        while not status.get_is_crc_ok():
            self.ser.write(cmd)
            status = self._wait_feedback(df.WRITE_OPCODE)
        list_of_statuses.append(status)

        # Read controlword
        status_1 = self.get_controlword()
        list_of_statuses.append(status_1)
        # TODO: check the controlword

        # Enable operation with new setpoint, immediately
        status_2 = dt.STATUS()
        cmd = self._command_maker.send_controlword(df.CW_SET_ENABLE_OP_IMMEDIATELY)
        while not status_2.get_is_crc_ok():
            self.ser.write(cmd)
            status_2 = self._wait_feedback(df.WRITE_OPCODE)
        list_of_statuses.append(status_2)

        # Enable operation
        status_3 = dt.STATUS()
        cmd = self._command_maker.send_controlword(df.CW_SET_ENABLE_OPERATIONS)
        while not status_3.get_is_crc_ok():
            self.ser.write(cmd)
            status_3 = self._wait_feedback(df.WRITE_OPCODE)

        list_of_statuses.append(status_3)

        return list_of_statuses

    def halt_position_movement(self):
        pass

    # State machine
    def get_fault_state(self) -> bool:
        status = self.get_statusword()
        return bool(status.get_returned_data()[-1].get() & df.SW_FAULT_BITS)

    def get_enable_state(self) -> bool:
        status = self.get_statusword()
        d = status.get_returned_data()[-1].get()
        if d & df.SW_ENABLE_STATE_BITS == df.SW_ENABLE_STATE_BITS:
            return True
        return False

    def set_enable_state(self) -> dt.ListOfStatuses:
        list_of_statuses = dt.ListOfStatuses()
        status = dt.STATUS(ss.OK)
        list_of_statuses.append(status)
        if self.get_enable_state():
            return list_of_statuses

        # Enable voltage and quick stop
        status_1 = dt.STATUS()
        cmd = self._command_maker.send_controlword(df.CW_SET_ENABLE_VOLT_AND_QUICK_STOP)
        while not status_1.get_is_crc_ok():
            self.ser.write(cmd)
            status_1 = self._wait_feedback(df.WRITE_OPCODE)
        list_of_statuses.append(status_1)

        # Set enable operations
        status_2 = dt.STATUS()
        cmd = self._command_maker.send_controlword(df.CW_SET_ENABLE_OPERATIONS)
        while not status_2.get_is_crc_ok():
            self.ser.write(cmd)
            status_2 = self._wait_feedback(df.WRITE_OPCODE)
        list_of_statuses.append(status_2)

        # Waiting while statusword match with 0x0437
        status_3 = dt.STATUS()
        for i in range(20):
            status_3 = self.get_statusword()
            ret_data = status_3.get_returned_data()
            if ret_data[2].get() & 0x04 and ret_data[3].get() & 0x37:
                break
        list_of_statuses.append(status_3)

        return list_of_statuses

    def close(self):
        self.ser.close()
