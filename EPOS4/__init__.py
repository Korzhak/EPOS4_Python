import serial
from EPOS4 import definitions as df
from EPOS4.EPOS4Common import EPOS4Common
from EPOS4.EPOS4CommandMaker import EPOS4CommandMaker
from EPOS4.EPOS4FeedbackParser import EPOS4FeedbackParser


class EPOS4:
    def __init__(self, com, baud_rate=115200, node_id=1):
        self.ser = serial.Serial(com, baud_rate)
        self._command_maker = EPOS4CommandMaker(node_id)
        self._feedback_parser = EPOS4FeedbackParser()

    def _wait_feedback(self, executed_feedback):
        first_time = True
        header = b''
        number_of_words = 0
        for i in range(1000):
            b = self.ser.inWaiting()
            if b:
                if first_time:
                    header = self.ser.read(4)
                    op_code, number_of_words = self._feedback_parser.parse_header(header)
                    first_time = False
                else:
                    # NoW - count of int16 values, but we received int8, so NoW must be multiplied by 2.
                    # And +2 it is CRC bytes
                    frame = self.ser.read(number_of_words*2+2)
                    resp = self._feedback_parser.read_obj_response(number_of_words, executed_feedback, header, frame)
                    first_time = True
                    return resp

    def get_statusword(self):
        cmd = self._command_maker.get_statusword()
        self.ser.write(cmd)
        return self._wait_feedback(df.READ_OPCODE)

    def get_operation_mode(self):
        cmd = self._command_maker.get_operation_mode()
        self.ser.write(cmd)
        return self._wait_feedback(df.READ_OPCODE)

    def set_operation_mode(self, op_mode: int):
        cmd = self._command_maker.set_operation_mode(op_mode)
        self.ser.write(cmd)
        return self._wait_feedback(df.WRITE_OPCODE)

    def move_to_position(self, position: int):
        cmd = self._command_maker.move_to_position(position)
        self.ser.write(cmd)
        return self._wait_feedback(df.WRITE_OPCODE)

    def close(self):
        self.ser.close()
