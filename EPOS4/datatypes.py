
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
    def __init__(self, status):
        self._status = 0
        self.set(status)

    def set(self, status):
        # TODO: make checking status
        self._status = status

    def get(self):
        return self._status

    def __eq__(self, other):
        return self._status == other.get()

    def __str__(self):
        return str(self._status)

    def __repr__(self):
        return str(self._status)
