
class BYTE:
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
    def __init__(self, val):
        super().__init__(val)

    def set(self, val):
        self._val = val & 0xFFFF


class DWORD(WORD):
    def __init__(self, val):
        super().__init__(val)

    def set(self, val):
        self._val = val & 0xFFFFFFFF
