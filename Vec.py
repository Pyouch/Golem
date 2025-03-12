from math import sqrt


class Vec:
    def __init__(self, *args):
        self.v = args

    def dim(self):
        return len(self.v)

    @property
    def x(self): return self.v[0]

    @property
    def y(self): return self.v[1]

    @property
    def z(self): return self.v[2]

    @property
    def w(self): return self.v[3]

    @property
    def r(self):
        return self.v[0]

    @property
    def g(self):
        return self.v[1]

    @property
    def b(self):
        return self.v[2]

    @property
    def a(self):
        return self.v[3]

    def get(self):
        return self.v

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.v[item]
        if isinstance(item, str):
            coordinates = {"x": 0, "y": 1, "z": 2, "w": 3, "r": 0, "g": 1, "b": 2, "a": 3, "0": None}
            v = []
            for e in item:
                assert e in coordinates, f"{e} is not a coordinate"
                if e == "0":
                    v.append(0)
                else:
                    v.append(self.v[coordinates[e]])
            return Vec(*v)

    def bi_operation(self, binary_op, other):
        v1 = list(self.get())
        v2 = list(other.get())
        for i in range(len(v1)):
            v1[i] = binary_op(v1[i], v2[i])
        return Vec(*v1)

    def un_operation(self, unary_op):
        v = list(self.get())
        for i in range(len(v)):
            v[i] = unary_op(v[i])
        return Vec(*v)

    def __add__(self, other):
        return self.bi_operation(lambda x, y: x + y, other)

    def __sub__(self, other):
        return self.bi_operation(lambda x, y: x - y, other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.un_operation(lambda x: x * other)
        elif isinstance(other, Vec):
            return self.bi_operation(lambda x, y: x * y, other)
        else:
            assert True

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.un_operation(lambda x: x * other)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.un_operation(lambda x: x / other)
        elif isinstance(other, Vec):
            return self.bi_operation(lambda x, y: x / y, other)
        else:
            assert True

    def __floordiv__(self, other):
        if isinstance(other, int):
            return self.un_operation(lambda x: x // other)
        elif isinstance(other, Vec):
            return self.bi_operation(lambda x, y: x // y, other)
        else:
            assert True

    def __mod__(self, other):
        return self.un_operation(lambda x: x % other)

    def __str__(self):
        return "vec" + str(self.v)

    def __repr__(self):
        return str(self)

    def __neg__(self):
        return self * (-1)

    def size(self):
        return sqrt(dot(self, self))

    def normalize(self):
        s = self.size()
        if s == 0:
            return Vec(*self.v)
        return self / s

    def rotate90(self):
        assert self.dim() == 2
        return Vec(self.y, -self.x)


def dot(v1, v2):
    res = 0
    v1 = v1.get()
    v2 = v2.get()
    assert len(v1) == len(v2)
    for i in range(len(v1)):
        res += v1[i] * v2[i]
    return res


def cross(v1, v2):
    """ v1 and v2 must be of dimension 3 """
    return Vec(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )


def dist(v1, v2):
    return (v1-v2).dim()


ZERO2 = Vec(0, 0)
UP2 = Vec(0, -1)
DOWN2 = Vec(0, 1)
RIGHT2 = Vec(1, 0)
LEFT2 = Vec(-1, 0)

ZERO3 = Vec(0, 0, 0)
UP3 = Vec(0, 0, -1)
DOWN3 = Vec(0, 0, 1)
RIGHT3 = Vec(1, 0)
LEFT3 = Vec(-1, 0)
FORWARD3 = Vec(0, 1, 0)
BACKWARD3 = Vec(0, -1, 0)
