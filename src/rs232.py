from epos4 import Epos4
from epos4 import definitions as df

e = Epos4('COM35')

print("Set op mode")
om = e.get_operation_mode().get()
if om != df.OM_PPM:
    print(f"Changing operation mode {om} to {df.OM_PPM}")
    print(repr(e.set_operation_mode(df.OM_PPM)))
print("Operation mode has been set")

print("Checking enable state")
if not e.get_enable_state():
    print(f"State is disabled.\nSetting enable state...")
    print(e.set_enable_state())

print(f"Driver has been set to enable state")

print("Moving to position:")
for i in range(0xF, 0xFFFF, 0xFF):
    print(e.move_to_position(i))  # <- Contains print inside method

print("Position has been reached")

e.close()

