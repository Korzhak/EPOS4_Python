
class BYTE:
    """
    BYTE is unsigned integer, 1 byte (8 bits)
    0..255
    """
    def __init__(self, val):
        self._val = 0
        self.set(val)

    def set(self, val):
        self._val = val & 0xFF

    def get(self):
        return self._val

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return self._val


class WORD(BYTE):
    """
    WORD is unsigned integer, 2 bytes (16 bits)
    0..65'535
    """
    def __init__(self, val):
        super().__init__(val)

    def set(self, val):
        self._val = val & 0xFFFF


class DWORD(WORD):
    """
    DOUBLE WORD is unsigned integer, 4 bytes (32 bits)
    0..4'294'967'295
    """
    def __init__(self, val):
        super().__init__(val)

    def set(self, val):
        self._val = val & 0xFFFFFFFF
