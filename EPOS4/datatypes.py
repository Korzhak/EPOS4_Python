
class BYTE:
    """
    BYTE is unsigned integer, 1 byte (8 bits)
    0..255
    """
    def __init__(self, val=0):
        self._val = 0
        self._len_of_bytes = 1
        self.set(val)

    def set(self, val):
        self._val = val & 0xFF

    def set_from_reversed_bytes(self, frame: bytes):
        if len(frame) != self._len_of_bytes:
            raise Exception(f"Length of frame must be {self._len_of_bytes}")
        bts = 0
        bts |= 0xFF & int(frame[0])
        self.set(bts)

    def get(self):
        return self._val

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return str(self._val)


class WORD(BYTE):
    """
    WORD is unsigned integer, 2 bytes (16 bits)
    0..65'535
    """
    def __init__(self, val=0):
        super().__init__(val)
        self._len_of_bytes = 2

    def set(self, val):
        self._val = val & 0xFFFF

    def set_from_reversed_bytes(self, frame: bytes):
        if len(frame) != self._len_of_bytes:
            raise Exception(f"Length of frame must be {self._len_of_bytes}")
        bts = 0
        bts |= 0xFF00 & (int(frame[1]) << 8)
        bts |= 0x00FF & int(frame[0])
        self.set(bts)


class DWORD(WORD):
    """
    DOUBLE WORD is unsigned integer, 4 bytes (32 bits)
    0..4'294'967'295
    """
    def __init__(self, val=0):
        super().__init__(val)
        self._len_of_bytes = 4

    def set(self, val):
        self._val = val & 0xFFFFFFFF

    def set_from_reversed_bytes(self, frame: bytes):
        if len(frame) != self._len_of_bytes:
            raise Exception(f"Length of frame must be {self._len_of_bytes}")
        bts = 0
        bts |= 0xFF000000 & (int(frame[3]) << 24)
        bts |= 0x00FF0000 & (int(frame[2]) << 16)
        bts |= 0x0000FF00 & (int(frame[1]) << 8)
        bts |= 0x000000FF & int(frame[0])
        self.set(bts)


class STATUS:
    def __init__(self, status: int = 0,
                 returned_error: DWORD = 0,
                 returned_data: list = None,
                 is_crc_ok: bool = None,
                 frame: list = None):
        self._status = 0
        self._returned_error = DWORD()
        self._returned_data = None
        self._is_crc_ok = None
        self._frame = None

        self.set_status(status)
        self.set_returned_error(returned_error)
        self.set_returned_data(returned_data)
        self.set_is_crc_ok(is_crc_ok)
        self.set_frame(frame)

    def set_status(self, status: int):
        # TODO: make checking status
        self._status = status

    def get_status(self) -> int:
        return self._status

    def set_returned_error(self, error: DWORD):
        # TODO: make checking error
        self._returned_error = error

    def get_returned_error(self) -> DWORD:
        return self._returned_error

    def set_returned_data(self, data: list):
        # TODO: make checking data
        self._returned_data = data

    def get_returned_data(self) -> list:
        return self._returned_data

    def set_is_crc_ok(self, is_crc_ok: bool):
        self._is_crc_ok = is_crc_ok

    def get_is_crc_ok(self) -> bool:
        return self._is_crc_ok

    def set_frame(self, frame: list):
        self._frame = frame

    def get_frame(self) -> list:
        return self._frame

    def __eq__(self, other):
        return self._status == other.get_status()

    def __str__(self):
        return str(self._status)

    def __repr__(self):
        if not self._returned_data:
            self._returned_data = []
        if not self._frame:
            self._frame = []
        if type(self._returned_error) == int:
            self._returned_error = DWORD(self._returned_error)
        return f"(Status: {self._status}, Returned error: {hex(self._returned_error.get())}, " \
               f"Returned data: {[hex(i.get()) for i in self._returned_data]}, Is CRC OK: {self._is_crc_ok}, " \
               f"Frame: {[hex(i) for i in self._frame]})"
