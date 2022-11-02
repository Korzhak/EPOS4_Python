from EPOS4 import datatypes as dt
from EPOS4 import definitions as df
from EPOS4 import statuses as ss
from EPOS4.EPOS4Common import EPOS4Common


class EPOS4FeedbackParser(EPOS4Common):
    def __init__(self):
        super(EPOS4FeedbackParser, self).__init__()

    def error_check(self, error_dword: dt.DWORD):
        pass

    @staticmethod
    def parse_header(header: bytes) -> len:
        """
        Parser of header
        :param header: 4 bytes of header
        :return: (two arguments) operation mode and number of words for next reading bytes
        """
        # TODO: return status
        if len(header) != 4:
            raise Exception("Header frame length must be 4 bytes")
        elif int(header[0]) != 0x90 and int(header[1]) != 0x02:
            raise Exception("Didn't receive start of frame")
        # elif int(header[2]) == 0x00:
        return int(header[2]), int(header[3])

    def read_obj_response(self, now: int, executed_opcode: int, header: bytes, frame: bytes) -> dt.STATUS:
        if len(frame) != (now * 2 + 2):
            return ss.ERROR_NUMBER_OF_WORDS

        full_frame = []
        for i in header:
            full_frame.append(int(i))
        for i in frame:
            full_frame.append(int(i))

        # Restuffing data
        # Removing doubled 0x90 bytes
        pure_frame = []
        preview_byte = 0
        for i in full_frame:
            # TODO: fixed it if 0x90 exist more then 2 times
            if i == 0x90 and preview_byte == 0x90:
                continue
            pure_frame.append(i)
            preview_byte = i

        # Calculating CRC and checking it
        crc = self.parse_and_calc_crc(pure_frame[2:-2])
        if self.restore_word(pure_frame[-2], pure_frame[-1]) != crc:
            return ss.ERROR_CRC

        print(f"CRC is OK: {hex(crc)}")

        # Getting error code from response data
        error_code = dt.DWORD()
        error_code.set_from_reversed_bytes(frame[:4])
        print(f"Error code: {error_code}")

        print([hex(i) for i in pure_frame])
        if error_code:
            # return error_code
            print(f"Error code: {error_code}")

        # Getting response data from frame
        bytes_array = []
        if executed_opcode == df.READ_OPCODE:

            bytes_array.append(dt.BYTE(pure_frame[-3]))
            bytes_array.append(dt.BYTE(pure_frame[-4]))
            bytes_array.append(dt.BYTE(pure_frame[-5]))
            bytes_array.append(dt.BYTE(pure_frame[-6]))

            print(bytes_array)
        # int_frame = []
        # for i in range(4):
        #     int_frame.append(int(frame[i]))


