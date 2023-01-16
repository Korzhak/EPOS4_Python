# -*- coding: utf-8 -*-
# Example 1. Working with Maxon EPOS4 through UART.
# Operation mode: Profile Position Mode
#  Date: 16.01.2023
#  Author: Korzhak (GitHub)
#  Ukraine
#

from epos4 import Epos4
from epos4 import definitions as df

e = Epos4('COM3')

om = e.get_operation_mode().get()
if om != df.OM_PPM:
    e.set_operation_mode(df.OM_PPM)

if not e.get_enable_state():
    e.set_enable_state()

if not e.get_fault_state():
    e.move_to_position(0xFFF)

e.close()
