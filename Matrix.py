from Vec import Vec, dot
from math import sqrt, cos, sin, pi
import numpy as np


class Matrix:
    def __init__(self, *args):
        self.mat = np.array([])
        if isinstance(args[0], int) or isinstance(args[0], float):
            size = int(sqrt(len(args)))
            self.mat = np.array(args)
            self.mat.shape = (size, size)

        elif isinstance(args[0], list) and len(args) == 1:
            self.mat = np.array(args[0])
            if 1 <= len(self.mat.shape) <= 2:
                raise RuntimeError("Une matrice doit être 2D (ou éventuellement 1D)")
        elif isinstance(args[0], np.ndarray) and len(args) == 1:
            if len(args[0].shape) == 1: self.mat = args[0].reshape((len(args[0]), 1))
            elif len(args[0].shape) == 2: self.mat = args[0]
            else: raise RuntimeError("Une matrice doit être 2D (ou éventuellement 1D)")

        elif isinstance(args[0], Vec):
            a = [v.get() for v in args]
            self.mat = np.array(a).transpose()

        elif isinstance(args[0], np.ndarray) or isinstance(args[0], list):
            size = len(args)
            self.mat = np.array(args)
            self.mat.shape = (size, size)
            

    def dim(self):
        return len(self.mat)

    def __mul__(self, other):
        """Do the matrix product between self and other"""
        if isinstance(other, Matrix):
            res = np.dot(self.mat, other.mat)
            return Matrix(res)
        elif isinstance(other, Vec):
            res = np.dot(self.mat, other.get().transpose())
            return Vec(res)

    def __str__(self):
        return str(self.mat)

    def transpose(self):
        return Matrix(np.transpose(self.mat))

    @classmethod
    def rotation_x(cls, theta):
        return cls(1, 0, 0, 0, cos(theta), -sin(theta), 0, sin(theta), cos(theta))

    @classmethod
    def rotation_y(cls, theta):
        return cls(cos(theta), 0, sin(theta), 0, 1, 0, -sin(theta), 0, cos(theta))

    @classmethod
    def rotation_z(cls, theta):
        return cls(cos(theta), sin(theta), 0, -sin(theta), cos(theta), 0, 0, 0, 1)


if __name__ == "__main__":
    m = Matrix(0, 1, 2, 3, 4, 5, 6, 7, 8)
    print(m)
    print(m.transpose())

    """m = Matrix(1, 2, 3, 4)
    print(m * m)

    m1 = Matrix.rotation_x(-pi / 4)
    m2 = Matrix.rotation_z(pi / 4)
    print(m1)
    print(m2)
    print(m2 * m1 * Vec(1, 0, 0))
    print(m2 * m1 * Vec(0, 1, 0))
    print(m2 * m1 * Vec(0, 0, 1))"""
