import serial
from EPOS4 import EPOS4
from EPOS4 import definitions as df


e = EPOS4('COM35')
# print("Get op mode:")
# print(repr(e.get_operation_mode()))
# print("-----------------")
# print("Set op mode:")
# print(repr(e.set_operation_mode(df.OM_PPM)))
# print("-----------------")
# print("Get op mode:")
# print(repr(e.get_operation_mode()))
# print("-----------------")
print("Get status word:")
print(repr(e.get_statusword()))
# print("-----------------")
# print("Get fault state:")
# print(e.get_fault_state())
# print("-----------------")
# print("Get enable state:")
# print(e.get_enable_state())
# print("-----------------")
# print("Set enable state:")
# print(repr(e.set_enable_state()))
# print("Set enable state:")
# print(repr(e.move_to_position(0xFF0F)))

e.close()

