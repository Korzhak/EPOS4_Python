from EPOS4.EPOS4CommandMaker import EPOS4CommandMaker
# from EPOS4 import Definitions
# from EPOS4 import datatypes

import serial


class EPOS4:
    def __init__(self, com, baud_rate=115200, node_id=1):
        self.ser = serial.Serial(com, baud_rate)
        self._command_maker = EPOS4CommandMaker(node_id)

    def _wait_feedback(self):
        for i in range(1000):
            b = self.ser.inWaiting()
            if b:
                print(self.ser.read(4))
                print(self.ser.read(10))

    def get_operation_mode(self):
        cmd = self._command_maker.get_operation_mode()
        self.ser.write(cmd)
        self._wait_feedback()


e = EPOS4('COM1')
e.get_operation_mode()
