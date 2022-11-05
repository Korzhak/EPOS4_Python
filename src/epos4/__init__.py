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
        first_time = True
        resp = None
        header = b''
        status = dt.STATUS()
        for i in range(1000):
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
        self.ser.write(cmd)
        return self._wait_feedback(df.READ_OPCODE)

    def get_controlword(self) -> dt.STATUS:
        cmd = self._command_maker.get_controlword()
        self.ser.write(cmd)
        return self._wait_feedback(df.READ_OPCODE)

    # Operation mode methods
    def get_operation_mode(self) -> dt.STATUS:
        cmd = self._command_maker.get_operation_mode()
        self.ser.write(cmd)
        return self._wait_feedback(df.READ_OPCODE)

    def set_operation_mode(self, op_mode: int) -> dt.STATUS:
        cmd = self._command_maker.set_operation_mode(op_mode)
        self.ser.write(cmd)
        return self._wait_feedback(df.WRITE_OPCODE)

    # PPM methods
    def get_position_profile(self):
        pass

    def set_position_profile(self):
        pass

    def get_target_position(self):
        pass

    def move_to_position(self, position: int) -> dt.STATUS:
        cmd = self._command_maker.move_to_position(position)
        self.ser.write(cmd)
        status = self._wait_feedback(df.WRITE_OPCODE)
        # if status.get_returned_error().get():
        #     status.set_status(ss.ERROR)
        #     return status
        print(repr(status))
        status = self.get_statusword()
        ret_data = status.get_returned_data()
        print(repr(status))
        # if not (ret_data[2].get() == 0x04 and ret_data[3].get() == 0x37):
        #     status.set_status(ss.ERROR)
        #     return status
        status = self.get_controlword()
        ret_data = status.get_returned_data()
        # if not (ret_data[3].get() == 0x0F):
        #     status.set_status(ss.ERROR)
        #     return status
        print(repr(status))
        cmd = self._command_maker.send_controlword(0x3F)
        self.ser.write(cmd)
        status = self._wait_feedback(df.WRITE_OPCODE)
        # if status.get_returned_error().get():
        #     status.set_status(ss.ERROR)
        #     return status
        status = self.get_statusword()
        ret_data = status.get_returned_data()
        # if not (ret_data[2].get() == 0x10 and ret_data[3].get() == 0x37):
        #     status.set_status(ss.ERROR)
        #     return status
        cmd = self._command_maker.send_controlword(0x0F)
        self.ser.write(cmd)
        status = self._wait_feedback(df.WRITE_OPCODE)
        # if status.get_returned_error().get():
        #     status.set_status(ss.ERROR)
        #     return status
        return status

    def halt_position_movement(self):
        pass

    # State machine
    def get_fault_state(self) -> bool:
        status = self.get_statusword()
        return bool(status.get_returned_data()[-1].get() & df.SW_FAULT_BITS)

    def get_enable_state(self) -> bool:
        status = self.get_statusword()
        return bool(status.get_returned_data()[-1].get() & df.SW_ENABLE_STATE_BITS)

    def set_enable_state(self) -> dt.STATUS:
        if self.get_enable_state():
            return dt.STATUS(ss.OK)
        cmd = self._command_maker.send_controlword(df.CW_SET_ENABLE_VOLT_AND_QUICK_STOP)
        self.ser.write(cmd)
        status = self._wait_feedback(df.WRITE_OPCODE)
        # # TODO: check status
        # # if not status.get_returned_error() == ss.OK:
        # # TODO: status error
        #     # pass
        status = self.get_statusword()
        # if not status.get_returned_data()[-1].get() == df.SW_READY_TO_SWITCH_ON:
        #     # TODO: if statusword
        #     pass
        cmd = self._command_maker.send_controlword(df.CW_SET_ENABLE_OPERATIONS)
        self.ser.write(cmd)
        status = self._wait_feedback(df.WRITE_OPCODE)
        for i in range(20):
            status = self.get_statusword()
            ret_data = status.get_returned_data()
            if ret_data[2].get() == 0x04 and ret_data[3].get() == 0x37:
                break
        #     # TODO: remove print
        return status

    def close(self):
        self.ser.close()
