from . import datatypes as dt
from . import definitions as df
from . import statuses as ss
from .common import Epos4Common


class Epos4FeedbackParser(Epos4Common):
    def __init__(self):
        super(Epos4FeedbackParser, self).__init__()

    def error_check(self, error_dword: dt.DWORD):
        # TODO: Checking error code and return explanation
        pass

    @staticmethod
    def parse_header(header: bytes) -> dt.STATUS:
        """
        Parser of header
        :param header: 4 bytes of header
        :return: (two arguments) operation mode and number of words for next reading bytes
        """
        if len(header) != 4:
            return dt.STATUS(ss.ERROR_HEADER_LENGTH)
        elif int(header[0]) != 0x90 and int(header[1]) != 0x02:
            return dt.STATUS(ss.ERROR_START_OF_FRAME)
        elif int(header[2]) != 0x00:
            return dt.STATUS(ss.ERROR_OPCODE)
        status = dt.STATUS(ss.OK)
        status.set_data_from_bytes(header)
        return status

    def read_obj_response(self, now: int, executed_opcode: int, header: bytes, frame: bytes) -> dt.STATUS:
        """
        Parsing obtained frame. Forming status object which contains obtained data, errors and status of executing
        :param now: number of word (NoW)
        :param executed_opcode: executed opcode before obtaining frame
        :param header: obtained first frame (contains response OpCode and NoW)
        :param frame: obtained second frame (contains errors, data and CRC)
        :return: status object with status of executing, errors and data
        """
        status = dt.STATUS(ss.OK)

        # Checking length of frame
        if len(frame) != (now * 2 + 2):
            return status.set_status(ss.ERROR_NUMBER_OF_WORDS)

        # Gluing header and frame data
        full_frame = []
        for i in header:
            full_frame.append(int(i))
        for i in frame:
            full_frame.append(int(i))

        # Restuffing data
        pure_frame = self.restuffing_data(full_frame)

        # Updating status object. Adding obtained data
        status.set_frame_from_list(pure_frame)

        # Calculating CRC and checking it
        crc = self.parse_and_calc_crc(pure_frame[2:-2])
        if self.restore_word(pure_frame[-2], pure_frame[-1]) != crc:
            # Updating status object that CRC is Fault and returning error status
            status.set_is_crc_ok(False)
            status.set_status(ss.ERROR_CRC)
            return status

        # Updating status object that CRC is OK
        status.set_is_crc_ok(True)

        # Getting error code from response data
        error_code = dt.DWORD()
        error_code.set_from_reversed_bytes(frame[:4])
        status.set_returned_error(error_code)

        # Getting response data from frame
        if executed_opcode == df.READ_OPCODE:
            status.set_returned_data_from_list(pure_frame[8:-2], reverse=True)

        # TODO: Processing other cases getting returned data with different length

        return status

