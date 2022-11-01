# -*- coding: utf-8 -*-
"""
Example to command EPOS4 with python
Operation Mode: Profile Position Mode, 10cycles repeated
No Homing

Python Version 3.7
Tested with Raspberry Pi 3

Created on 24.02.2021
Version 1.0
@author: CCMC, maxon motor ag, Switzerland

"""

from ctypes import *

# sleep function
import time

# Folder created for example: /home/pi/src/python/
# Copy maxon motor Linux Library arm v7 into this folder
# Library must match according your cpu, eg. PI3 has arm v7
# EPOS Comand Library can be found here, when EPOS Studio has been installed:
# C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Linux Library
path = 'C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll'
cdll.LoadLibrary(path)
epos = CDLL(path)

# Node ID must match with Hardware Dip-Switch setting of EPOS4
NodeID = 1
keyhandle = 0
# return variable from Library Functions
ret = 0
pErrorCode = c_uint()
pDeviceErrorCode = c_uint()


## ============================================================================================
# Read Statusword and mask it to bit12
def WaitAcknowledged():
    ObjectIndex = 0x6041
    ObjectSubindex = 0x0
    NbOfBytesToRead = 0x02
    pNbOfBytesRead = c_uint()
    pData = c_uint()
    pErrorCode = c_uint()

    # Setpoint Acknowledged
    Mask_Bit12 = 0x1000
    Bit12 = 0
    i = 0

    while True:
        # Read Statusword
        ret = epos.VCS_GetObject(keyhandle, NodeID, ObjectIndex, ObjectSubindex, byref(pData), NbOfBytesToRead,
                                 byref(pNbOfBytesRead), byref(pErrorCode))
        Bit12 = Mask_Bit12 & pData.value

        # Timed out
        if i > 20:
            return 0
            break

        if Bit12 == Mask_Bit12:
            time.sleep(1)
            i += 1

        # Bit12 reseted = new profile started
        else:
            return 1
            break


def CyclicMode(pErrorCode):
    print('Wait finishing positioning...')

    for x in range(1, 11):
        print('Loop: %d' % x)

        # TargetPosition=20'000qc / AbsolutMovement=0 =>Relative Positioning / StartProfileImmediately=0
        ret = epos.VCS_MoveToPosition(keyhandle, NodeID, 20000, 0, 0, byref(pErrorCode))

        ret = WaitAcknowledged()

        # Send new profile during execution of previous profile
        ret = epos.VCS_MoveToPosition(keyhandle, NodeID, -20000, 0, 0, byref(pErrorCode))

        ret = WaitAcknowledged()

    print('Cyclic movemenent finished')

    return 1


# Example of using VCS_GetObject()
# With this function any CANopen Object can be accessed
def GetPosition():
    # CANopen Object: Position Actual Value
    ObjectIndex = 0x6064
    ObjectSubIndex = 0x00
    NbOfBytesToRead = 0x04
    # DWORD
    NbOfBytesRead = c_uint()
    # 0x6064 => INT32
    pData = c_int()
    pErrorCode = c_uint()

    ret = epos.VCS_GetObject(keyhandle, NodeID, ObjectIndex, ObjectSubIndex, byref(pData), NbOfBytesToRead,
                             byref(NbOfBytesRead), byref(pErrorCode))

    if ret == 1:
        print('Position Actual Value: %d [inc]' % pData.value)
        return 1
    else:
        print('GetObject failed')
        return 0


# Get Position direct via function
def GetPositionIs():
    pPositionIs = c_long()
    pErrorCode = c_uint()

    ret = epos.VCS_GetPositionIs(keyhandle, NodeID, byref(pPositionIs), byref(pErrorCode))

    if ret == 1:
        print('Position Actual Value: %d [inc]' % pPositionIs.value)
        return 1
    else:
        print('GetPositionIs failed')
        return 0


## ============================================================================================
# Main
# Open USB Port
print('Opening Port...')
keyhandle = epos.VCS_OpenDevice(b'EPOS4', b'MAXON SERIAL V2', b'USB', b'USB0', byref(pErrorCode))

if keyhandle != 0:

    print('Keyhandle: %8d' % keyhandle)

    # Verify Error State of EPOS4
    ret = epos.VCS_GetDeviceErrorCode(keyhandle, NodeID, 1, byref(pDeviceErrorCode), byref(pErrorCode))
    print('Device Error: %#5.8x' % pDeviceErrorCode.value)

    # Device Error Evaluation
    if pDeviceErrorCode.value == 0:

        # Set Operation Mode PPM
        ret = epos.VCS_ActivateProfilePositionMode(keyhandle, NodeID, byref(pErrorCode))

        # Profile Velocity=500rpm / Acceleration=1000rpm/s / Deceleration=1000rpm/s
        ret = epos.VCS_SetPositionProfile(keyhandle, NodeID, 500, 1000, 1000, byref(pErrorCode))

        # Read Position Actual Value with VCS_GetObject()
        ret = GetPosition()

        ret = epos.VCS_SetEnableState(keyhandle, NodeID, byref(pErrorCode))
        print('Device Enabled')

        ret = CyclicMode(pErrorCode)

        ret = epos.VCS_SetDisableState(keyhandle, NodeID, byref(pErrorCode))
        print('Device Disabled')

        # Other Option to Read Position
        ret = GetPositionIs()

    else:
        print('EPOS4 is in Error State: %#5.8x' % pDeviceErrorCode.value)
        print('EPOS4 Error Description can be found in the EPOS4 Fimware Specification')

    # Close Com-Port
    ret = epos.VCS_CloseDevice(keyhandle, byref(pErrorCode))
    print('Error Code Closing Port: %#5.8x' % pErrorCode.value)

else:
    print('Could not open Com-Port')
    print('Keyhandle: %8d' % keyhandle)
    print('Error Openening Port: %#5.8x' % pErrorCode.value)
