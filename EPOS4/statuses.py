from EPOS4 import datatypes as dt

# Everything is OK
OK = dt.STATUS(0)

# Header frame length must be 4 bytes
ERROR_HEADER_LENGTH = dt.STATUS(10)

# Didn't receive start of frame
ERROR_START_OF_FRAME = dt.STATUS(11)

# Length of frame does not response passed number of words
# Length of frame must be x2 of number of words
ERROR_NUMBER_OF_WORDS = dt.STATUS(12)

# CRC is not right
ERROR_CRC = dt.STATUS(13)

RETURNED_ERRORS = dt.STATUS(51)
