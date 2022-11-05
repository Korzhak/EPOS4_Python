from . import datatypes as dt
from . import definitions as df
from . import statuses as ss
from .common import Epos4Common


class Epos4FeedbackParser(Epos4Common):
    def __init__(self):
        super(Epos4FeedbackParser, self).__init__()

    def error_check(self, error_dword: dt.DWORD):
        pass

    @staticmethod
    def parse_header(header: bytes) -> dt.STATUS:
        """
        Parser of header
        :param header: 4 bytes of header
        :return: (two arguments) operation mode and number of words for next reading bytes
        """
        # TODO: return status
        if len(header) != 4:
            return dt.STATUS(ss.ERROR_HEADER_LENGTH)
        elif int(header[0]) != 0x90 and int(header[1]) != 0x02:
            return dt.STATUS(ss.ERROR_START_OF_FRAME)
        # elif int(header[2]) == 0x00:
        status = dt.STATUS(ss.OK)
        status.set_data_from_bytes(header)
        return status

    def read_obj_response(self, now: int, executed_opcode: int, header: bytes, frame: bytes) -> dt.STATUS:
        status = dt.STATUS()
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

        status.set_frame(pure_frame)

        # Calculating CRC and checking it
        crc = self.parse_and_calc_crc(pure_frame[2:-2])
        if self.restore_word(pure_frame[-2], pure_frame[-1]) != crc:
            status.set_is_crc_ok(False)
            status.set_status(ss.ERROR_CRC)
            return status

        status.set_is_crc_ok(True)

        # Getting error code from response data
        error_code = dt.DWORD()
        error_code.set_from_reversed_bytes(frame[:4])

        status.set_returned_error(error_code)

        if error_code:
            # TODO: checking error code
            pass

        # Getting response data from frame
        bytes_array = []
        if executed_opcode == df.READ_OPCODE:
            bytes_array.append(dt.BYTE(pure_frame[-3]))
            bytes_array.append(dt.BYTE(pure_frame[-4]))
            bytes_array.append(dt.BYTE(pure_frame[-5]))
            bytes_array.append(dt.BYTE(pure_frame[-6]))

            status.set_returned_data(bytes_array)

        status.set_status(ss.OK)
        return status

