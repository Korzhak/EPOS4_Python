# Everything is OK
OK = 0

# Unexpected error
ERROR = 1

# === Obtained frame processing errors ===
# Header frame length must be 4 bytes
ERROR_HEADER_LENGTH = 10

# Didn't receive start of frame
ERROR_START_OF_FRAME = 11

# Returned OpCode must be 0x00
ERROR_OPCODE = 12

# Length of frame does not response passed number of words
# Length of frame must be x2 of number of words
ERROR_NUMBER_OF_WORDS = 13

# CRC is not right
ERROR_CRC = 19

# === Other errors ===
RETURNED_ERRORS = 51
