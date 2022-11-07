
# Operation codes
READ_OPCODE = 0x60
WRITE_OPCODE = 0x68

# Number of words
READ_OPCODE_NoW = 0x02
WRITE_OPCODE_NoW = 0x04

# === INDEXES AND SUBINDEXES ===
# DOCS: Firmware Specification
#       2.2.3, 15 pg.
INDEX_CONTROLWORD = 0x6040
INDEX_STATUSWORD = 0x6041

CW_SET_ENABLE_VOLT_AND_QUICK_STOP = 0x06
CW_SET_ENABLE_OPERATIONS = 0x0F
CW_SET_ENABLE_OP_IMMEDIATELY = 0x3F
SW_ENABLE_STATE_BITS = 0x7
SW_FAULT_BITS = 0x8
SW_READY_TO_SWITCH_ON = 0x21

# Operation Mode
INDEX_OM_SET_OPERATION_MODE = 0x6060
INDEX_OM_GET_OPERATION_MODE = 0x6061

# DOCS: Firmware Specification
#       6.2.91, 203 pg.
OM_PPM = 0x01
OM_PVM = 0x03
OM_HMM = 0x06
OM_CSP = 0x08
OM_CSV = 0x09
OM_CST = 0x0A


# Profile Position Mode
INDEX_PPM_PROFILE_VELOCITY = 0x6081
INDEX_PPM_PROFILE_ACCELERATION = 0x6083
INDEX_PPM_PROFILE_DECELERATION = 0x6084
INDEX_PPM_PROFILE_POSITION = 0x607A

BLANK_SUBINDEX = 0x00
