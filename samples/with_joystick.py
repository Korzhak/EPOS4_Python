from epos4 import Epos4
from epos4 import definitions as df
import pygame

pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()

preview_axis = 0

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
        # JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        axes = joystick.get_numaxes()

        # for i in range(axes):
        axis = joystick.get_axis(3)
        if axis != preview_axis:
            print(e.move_to_position(int((axis*100 + 250) * 500)))
        preview_axis = axis

    clock.tick(20)
