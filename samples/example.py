from epos4 import Epos4
from epos4 import definitions as df

e = Epos4('COM30')


def move(val):
    if e.get_fault_state():
        print("Fault state!")
        print(repr(e.clear_fault_state()))
    if not e.get_enable_state():
        print(f"State is disabled.\nSetting enable state...")
        print(e.set_enable_state())
    print(e.move_to_position(val))  # <- Contains print inside method


if __name__ == "__main__":
    # Setting operation mode
    print("Set op mode")
    om = e.get_operation_mode().get()
    if om != df.OM_PPM:
        print(f"Changing operation mode {om} to {df.OM_PPM}")
        print(repr(e.set_operation_mode(df.OM_PPM)))
    print("Operation mode has been set")

    # Setting enable state
    print("Checking enable state")
    if not e.get_enable_state():
        print(f"State is disabled.\nSetting enable state...")
        print(e.set_enable_state())
    print(f"Driver has been set to enable state")

    # Moving to position
    print("Moving to position:")
    try:
        for i in range(0xF, 0xFFFF, 0xFF):
            move(i)

    # Closing connection
    except KeyboardInterrupt:
        e.close()

