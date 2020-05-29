import struct


class Fmt:
    """
    Maps between low-level entities to their related property
    """
    ID = '<Q'
    NAME_LENGTH = '<I'
    BIRTH = 'I'
    GENDER = 'c'
    TIME = 'Q'
    TRANSFORM = 'ddd'
    ROTATE = 'dddd'
    WIDTH_HIGHT = 'II'
    FEELING = 'ffff'
    USR = 'user {0}: {1}, born {2} ({3})'
    SNPT = 'Snapshot from {0} on ({1}, {2}, {3}) / \
    ({4}, {5}, {6}, {7}) \
    with {8}X{9} color image and a {10}X{11} depth image'

    @classmethod
    def ARR(cls, length):
        return '<{0}s'.format(length)


class Unpack:

    """
    Unpacks accrording to Fmt mapping the data from the samples
    """
    def __init__(self, data):
        self.data = data

    def id(self):
        return struct.unpack(Fmt.ID, self.data.read(4))[0]

    def name_length(self):
        return struct.unpack(Fmt.NAME_LENGTH, self.data.read(4))[0]

    def arr(self, l):
        byte_name = struct.unpack(Fmt.ARR(l), self.data.read(l))
        return byte_name[0]

    def name(self, l):
        return self.arr(l).decode("utf-8")

    def birth(self):
        return struct.unpack(Fmt.BIRTH, self.data.read(4))[0]

    def gender(self):
        char_gender = struct.unpack(Fmt.GENDER, self.data.read(1))[0]
        gender = char_gender.decode("utf-8")
        return gender

    def time(self):
        return struct.unpack(Fmt.TIME, self.data.read(8))[0]

    def transform(self):
        return struct.unpack(Fmt.TRANSFORM, self.data.read(24))

    def rotation(self):
        return struct.unpack(Fmt.ROTATE, self.data.read(32))

    def image_size(self):
        return struct.unpack(Fmt.WIDTH_HIGHT, self.data.read(8))

    def feeling(self):
        return struct.unpack(Fmt.FEELING, self.data.read(16))
