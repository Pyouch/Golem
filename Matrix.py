from Vec import Vec, dot
from math import sqrt, cos, sin, pi


class Matrix:
    def __init__(self, *args):
        self.mat = []
        if isinstance(args[0], int) or isinstance(args[0], float):
            size = int(sqrt(len(args)))
            self.mat = [[0 for _ in range(size)] for _ in range(size)]
            for j in range(size):
                for i in range(size):
                    self.mat[j][i] = args[i+j*size]

        elif isinstance(args[0], Vec):
            size = len(args)
            self.mat = [[0 for _ in range(size)] for _ in range(size)]
            for j in range(size):
                for i in range(size):
                    self.mat[j][i] = args[i][j]
        elif isinstance(args[0], list) and len(args) == 1:
            self.mat = args[0]
        elif isinstance(args[0], list):
            size = len(args)
            self.mat = [[0 for _ in range(size)] for _ in range(size)]
            for j in range(size):
                for i in range(size):
                    self.mat[j][i] = args[j][i]

    def dim(self):
        return len(self.mat)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            assert other.dim() == self.dim()
            res = [[0 for _ in range(self.dim())] for _ in range(self.dim())]
            for i in range(self.dim()):
                for j in range(self.dim()):
                    for k in range(self.dim()):
                        res[i][j] += self.mat[i][k] * other.mat[k][j]
            return Matrix(res)
        elif isinstance(other, Vec):
            assert other.dim() == self.dim()
            res = []
            for i in range(self.dim()):
                res.append(dot(Vec(*self.mat[i]), other))
            return Vec(*res)

    def __str__(self):
        return str(self.mat)

    def transpose(self):
        mat = [[0 for _ in range(self.dim())] for _ in range(self.dim())]
        for i in range(self.dim()):
            for j in range(self.dim()):
                mat[i][j] = self.mat[j][i]
        return Matrix(mat)

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

    m = Matrix(1, 2, 3, 4)
    print(m * m)

    m1 = Matrix.rotation_x(-pi / 4)
    m2 = Matrix.rotation_z(pi / 4)
    print(m1)
    print(m2)
    print(m2 * m1 * Vec(1, 0, 0))
    print(m2 * m1 * Vec(0, 1, 0))
    print(m2 * m1 * Vec(0, 0, 1))
