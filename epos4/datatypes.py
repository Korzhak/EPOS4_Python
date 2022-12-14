
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
        self._val = int(val) & 0xFF

    def get(self):
        return self._val

    def __eq__(self, other):
        if isinstance(other, BYTE):
            return self._val == other._val
        else:
            raise ValueError("BYTE allowed only")

    def __ge__(self, other):
        if isinstance(other, BYTE):
            return self._val >= other._val
        else:
            raise ValueError("BYTE allowed only")

    def __gt__(self, other):
        if isinstance(other, BYTE):
            return self._val > other._val
        else:
            raise ValueError("BYTE allowed only")

    def __le__(self, other):
        if isinstance(other, BYTE):
            return self._val <= other._val
        else:
            raise ValueError("BYTE allowed only")

    def __lt__(self, other):
        if isinstance(other, BYTE):
            return self._val < other._val
        else:
            raise ValueError("BYTE allowed only")

    def __ne__(self, other):
        if isinstance(other, BYTE):
            return self._val != other._val
        else:
            raise ValueError("BYTE allowed only")

    def __rshift__(self, other):
        if isinstance(other, BYTE):
            return BYTE(self._val >> other._val)
        else:
            raise ValueError("BYTE allowed only")

    def __rrshift__(self, other):
        if isinstance(other, BYTE):
            return BYTE(other._val >> self._val)
        else:
            raise ValueError("BYTE allowed only")

    def __lshift__(self, other):
        if isinstance(other, BYTE):
            return BYTE(self._val << other._val)
        else:
            raise ValueError("BYTE allowed only")

    def __rlshift__(self, other):
        if isinstance(other, BYTE):
            return BYTE(other._val << self._val)
        else:
            raise ValueError("BYTE allowed only")

    def __or__(self, other):
        if isinstance(other, BYTE):
            return BYTE(self._val | other._val)
        else:
            raise ValueError("BYTE allowed only")

    def __ror__(self, other):
        if isinstance(other, BYTE):
            return BYTE(other._val | self._val)
        else:
            raise ValueError("BYTE allowed only")

    def __xor__(self, other):
        if isinstance(other, BYTE):
            return BYTE(self._val ^ other._val)
        else:
            raise ValueError("BYTE allowed only")

    def __rxor__(self, other):
        if isinstance(other, BYTE):
            return BYTE(other._val ^ self._val)
        else:
            raise ValueError("BYTE allowed only")

    def __invert__(self):
        return BYTE(~self._val)

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return hex(self._val)


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

    def __rshift__(self, other):
        if isinstance(other, WORD):
            return WORD(self._val >> other._val)
        else:
            raise ValueError("WORD allowed only")

    def __rrshift__(self, other):
        if isinstance(other, WORD):
            return WORD(other._val >> self._val)
        else:
            raise ValueError("WORD allowed only")

    def __lshift__(self, other):
        if isinstance(other, WORD):
            return WORD(self._val << other._val)
        else:
            raise ValueError("WORD allowed only")

    def __rlshift__(self, other):
        if isinstance(other, WORD):
            return WORD(other._val << self._val)
        else:
            raise ValueError("WORD allowed only")

    def __or__(self, other):
        if isinstance(other, WORD):
            return WORD(self._val | other._val)
        else:
            raise ValueError("WORD allowed only")

    def __ror__(self, other):
        if isinstance(other, WORD):
            return WORD(other._val | self._val)
        else:
            raise ValueError("WORD allowed only")

    def __xor__(self, other):
        if isinstance(other, WORD):
            return WORD(self._val ^ other._val)
        else:
            raise ValueError("WORD allowed only")

    def __rxor__(self, other):
        if isinstance(other, WORD):
            return WORD(other._val ^ self._val)
        else:
            raise ValueError("WORD allowed only")

    def __invert__(self):
        return WORD(~self._val)


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

    def __rshift__(self, other):
        if isinstance(other, DWORD):
            return DWORD(self._val >> other._val)
        else:
            raise ValueError("DWORD allowed only")

    def __rrshift__(self, other):
        if isinstance(other, DWORD):
            return DWORD(other._val >> self._val)
        else:
            raise ValueError("DWORD allowed only")

    def __lshift__(self, other):
        if isinstance(other, DWORD):
            return DWORD(self._val << other._val)
        else:
            raise ValueError("DWORD allowed only")

    def __rlshift__(self, other):
        if isinstance(other, DWORD):
            return DWORD(other._val << self._val)
        else:
            raise ValueError("DWORD allowed only")

    def __or__(self, other):
        if isinstance(other, DWORD):
            return DWORD(self._val | other._val)
        else:
            raise ValueError("DWORD allowed only")

    def __ror__(self, other):
        if isinstance(other, DWORD):
            return DWORD(other._val | self._val)
        else:
            raise ValueError("DWORD allowed only")

    def __xor__(self, other):
        if isinstance(other, DWORD):
            return DWORD(self._val ^ other._val)
        else:
            raise ValueError("DWORD allowed only")

    def __rxor__(self, other):
        if isinstance(other, DWORD):
            return DWORD(other._val ^ self._val)
        else:
            raise ValueError("DWORD allowed only")

    def __invert__(self):
        return DWORD(~self._val)


class ListOfBytes(list):
    def __init__(self):
        super(ListOfBytes, self).__init__()

    def append(self, item) -> None:
        if isinstance(item, BYTE):
            super(ListOfBytes, self).append(item)
        else:
            raise ValueError('BYTE allowed only')

    def insert(self, index, item):
        if isinstance(item, BYTE):
            super(ListOfBytes, self).insert(index, item)
        else:
            raise ValueError('BYTE allowed only')

    def __add__(self, item):
        if isinstance(item, ListOfBytes):
            super(ListOfBytes, self).__add__(item)
        else:
            raise ValueError('ListOfBytes allowed only')

    def __iadd__(self, item):
        if isinstance(item, ListOfBytes):
            super(ListOfBytes, self).__iadd__(item)
        else:
            raise ValueError('ListOfBytes allowed only')

    def __repr__(self):
        return f"{[hex(i.get()) for i in self]}"


class ListOfStatuses(list):
    def __init__(self):
        super(ListOfStatuses, self).__init__()

    def append(self, item) -> None:
        if isinstance(item, STATUS):
            super(ListOfStatuses, self).append(item)
        else:
            raise ValueError('STATUS allowed only')

    def insert(self, index, item):
        if isinstance(item, STATUS):
            super(ListOfStatuses, self).insert(index, item)
        else:
            raise ValueError('STATUS allowed only')

    def __add__(self, item):
        if isinstance(item, ListOfStatuses):
            super(ListOfStatuses, self).__add__(item)
        else:
            raise ValueError('ListOfStatuses allowed only')

    def __iadd__(self, item):
        if isinstance(item, ListOfStatuses):
            super(ListOfStatuses, self).__iadd__(item)
        else:
            raise ValueError('ListOfStatuses allowed only')

    def __str__(self):
        return f"{[repr(i) for i in self]}"

    def __repr__(self):
        return f"{[repr(i) for i in self]}"


class STATUS:
    def __init__(self, status: int = 0,
                 returned_error: DWORD = 0,
                 returned_data: ListOfBytes = None,
                 is_crc_ok: bool = None,
                 frame: ListOfBytes = None):
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

    def set_returned_data(self, data: ListOfBytes):
        self._returned_data = ListOfBytes()
        if isinstance(data, ListOfBytes):
            self._returned_data = data
        elif isinstance(data, list):
            self.set_returned_data_from_list(data)
        elif data is None:
            self._returned_data = None
        else:
            raise ValueError("Returned data value type must be ListOfBytes or list")

    def set_returned_data_from_list(self, data: list, reverse: bool = False):
        self._returned_data = ListOfBytes()
        if reverse:
            data.reverse()
        for i in data:
            if type(i) == BYTE:
                self._returned_data.append(i)
            else:
                self._returned_data.append(BYTE(i))

    def get_returned_data(self) -> ListOfBytes:
        return self._returned_data

    def set_is_crc_ok(self, is_crc_ok: bool):
        self._is_crc_ok = is_crc_ok

    def get_is_crc_ok(self) -> bool:
        return self._is_crc_ok

    def set_frame(self, frame: ListOfBytes):
        if isinstance(frame, ListOfBytes):
            self._frame = frame
        elif isinstance(frame, list):
            self.set_frame_from_list(frame)
        elif frame is None:
            self._frame = None
        else:
            raise ValueError("Frame value type must be ListOfBytes or list")

    def set_frame_from_list(self, frame: list, reverse: bool = False):
        """
        TODO: make description of method
        :param frame:
        :param reverse:
        :return:
        """
        self._frame = ListOfBytes()
        if reverse:
            frame.reverse()
        for i in frame:
            if type(i) == BYTE:
                self._frame.append(i)
            else:
                self._frame.append(BYTE(i))

    def get_frame(self) -> ListOfBytes:
        return self._frame

    def set_data_from_bytes(self, bts: bytes):
        lob = ListOfBytes()
        for i in bts:
            lob.append(BYTE(i))
        self.set_returned_data(lob)

    def __eq__(self, other):
        return self._status == other.get_status()

    def __str__(self):
        return str(self._status)

    def __repr__(self):
        if not self._returned_data:
            self._returned_data = ListOfBytes()
        if not self._frame:
            self._frame = ListOfBytes()
        return f"(Status: {self._status}, Returned error: {repr(self._returned_error)}, " \
               f"Returned data: {repr(self._returned_data)}, Is CRC OK: {self._is_crc_ok}, " \
               f"Frame: {repr(self._frame)})"
