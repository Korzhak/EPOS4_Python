import serial
from EPOS4 import EPOS4CommandMaker
import time

ser = serial.Serial('COM10', 115200)
epos4 = EPOS4CommandMaker.EPOS4CommandMaker(1)

# frame = epos4.set_operation_mode(0x01)
# ser.write(frame)
#
# frame = epos4.set_enable_state()
# ser.write(frame)
# time.sleep(2)

frame = epos4.move_to_position(0x0FF)
ser.write(frame)
time.sleep(0.01)

frame = epos4.send_controlword(0x3f)
ser.write(frame)
time.sleep(0.01)

frame = epos4.send_controlword(0x0f)
ser.write(frame)
time.sleep(0.01)
# frame = epos4.set_position_profile_deceleration(0x000003E8)
# frame = epos4.get_position_profile()
# frame = epos4.get_target_position()

# ser.write(b'\x90\x02\x60\x02\x01\x10\x20\x00\x69\x9A')

# a = [0x0468, 0x8101, 0x0060, 0x03e8, 0x0000, 0x0000]
# print([hex(i) for i in a])
# print(hex(epos4._calc_crc(a)))
# print("-------------------")
# b = [0x68, 0x4, 0x1, 0x81, 0x60, 0x0, 0xe8, 0x3, 0x0, 0x0]
# print(hex(epos4._parse_and_calc_crc(b)))
# print("-------------------")
# frame = epos4.set_position_profile_velocity(0x000003E8)
# print([hex(i) for i in frame])
# print("-------------------")
# frame = epos4.get_position_profile()
print([hex(i) for i in frame])
# ser.write(frame)
#
# for i in range(1000):
#     b = ser.inWaiting()
#     if b:
#         print(ser.read(4))
#         print(ser.read(10))
#
#
# ser.close()

"""
['0x468', '0x8301', '0x60', '0x3e8', '0x0', '0x0']
['0x90', '0x2', '0x68', '0x4', '0x1', '0x83', '0x60', '0x0', '0xe8', '0x3', '0x0', '0x0', '0xea', '0x7a']
"""


