from math import sqrt
import numpy as np


def _extract_ndarray(other):
    if isinstance(other, Vec): return other.v
    else: return other


class Vec:
    def __init__(self, *args):
        self.isInt = True
        if isinstance(args[0], np.ndarray):
            if len(args[0].shape) != 1:
                raise RuntimeError("Vec doit être un ndarray de dimension 2")
            self.v = args[0]
            self.isInt = isinstance(args[0][0], np.signedinteger)

        elif isinstance(args[0], float) or isinstance(args[0], int):
            self.v = np.array(args)
            self.isInt = isinstance(args[0], int)

        else:
            raise RuntimeError("Arguments invalides")

    def dim(self):
        """ Return the dimension of the vector """
        return len(self.v)

    def _int_or_float(self, elt):
        if self.isInt: return int(elt)
        else: return float(elt)

    @property
    def x(self): return self._int_or_float(self.v[0])

    @property
    def y(self): return self._int_or_float(self.v[1])

    @property
    def z(self): return self._int_or_float(self.v[2])

    @property
    def w(self): return self._int_or_float(self.v[3])

    @property
    def r(self):
        """Return the vector's red composant"""
        return self._int_or_float(self.v[0])

    @property
    def g(self):
        """Return the vector's green composant"""
        return self._int_or_float(self.v[1])

    @property
    def b(self):
        """Return the vector's blue composant"""
        return self._int_or_float(self.v[2])

    @property
    def a(self):
        """Return the vector's alpha composant"""
        return self._int_or_float(self.v[3])

    def get(self):
        return self.v

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.v[item]
        if isinstance(item, str):
            coordinates = {"x": 0, "y": 1, "z": 2, "w": 3, "r": 0, "g": 1, "b": 2, "a": 3, "0": None, "1": None}
            v = []
            for e in item:
                assert e in coordinates, f"{e} is not a coordinate"
                if e == "0":
                    v.append(0)
                elif e == "1":
                    v.append(1)
                else:
                    v.append(self.v[coordinates[e]])
            return Vec(*v)

    def __add__(self, other):
        return Vec(self.v + _extract_ndarray(other))

    def __sub__(self, other):
        return Vec(self.v - _extract_ndarray(other))

    def __mul__(self, other):
        return Vec(self.v * _extract_ndarray(other))

    def __rmul__(self, other):
        return self * _extract_ndarray(other)

    def __truediv__(self, other):
        return Vec(self.v / _extract_ndarray(other))

    def __floordiv__(self, other):
        return Vec(self.v // _extract_ndarray(other))

    def __mod__(self, other):
        return Vec(self.v % _extract_ndarray(other))

    def __str__(self):
        return "vec" + str(self.v)

    def __repr__(self):
        return str(self)

    def __neg__(self):
        return self * (-1)

    def size(self):
        """ Return the norm of the vector """
        return sqrt(dot(self, self))

    def normalize(self):
        """ Return the vector normalized """
        s = self.size()
        if s == 0:
            return Vec(*self.v)
        return self / s

    def rotate90(self):
        """ Rotate the vector anti-clockwise """
        assert self.dim() == 2
        return Vec(self.y, -self.x)
    
    def add_dim(self, comp=0):
        """Add a dimension to the vector with the composant 0 if not presized"""
        return Vec(np.append(self.v, comp))

    def remove_dim(self, nb_dims=1):
        """Remove the vector's last dimension"""
        return Vec(self.v[:-nb_dims])

    def to_int(self):
        """ returns a Vec of ints instead of a Vec of floats """
        return Vec(np.int64(self.v))

    def to_float(self):
        """ returns a Vec of floats instead of a Vec of ints """
        return Vec(np.float64(self.v))

    def __hash__(self):
        return hash(tuple(self.get()))


def dot(v1, v2):
    """ Return the dot product of v1 and v2 """
    return np.sum(v1.get() * v2.get())


def cross(v1, v2):
    """ Return the cross product of v1 and v2
    v1 and v2 must be of dimension 3 """
    return Vec(np.cross(v1.get(), v2.get()))


def dist(v1, v2):
    """ Returns the distance between v1 and v2 """
    return (v1-v2).size()


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

if __name__ == "__main__":
    test = Vec(2,3)
    #print(test.dim())
    test.add_dim(1)
    #print(test.dim(), test)
    #test.remove_dim()
    #print(test.dim(), test)
    print(dot(test, test))
    