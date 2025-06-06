from GraphicPrimitives import *
from Matrix import *


class Primitive3D:
    def __init__(self, pos: Vec, size: int = 0):
        """
        :param pos: The position of the middle of the primitive
        :param size: The distance between the position and the most far point of
        the primitive.
        """
        self.pos = pos
        self.size = size

    def to_2d(self, engine, vertices: list[Vec], col_infos: list[tuple[Vec, Vec, Vec]]) -> Primitive2D:
        pass

    def split(self):
        return []

    def splittable(self):
        return False

    def finalize(self):
        pass

    def translate(self, vec):
        self.pos += vec

    def rotateX(self, angle):
        self.apply_matrix_3x3(Matrix.rotation_x(angle))

    def rotateY(self, angle):
        self.apply_matrix_3x3(Matrix.rotation_y(angle))

    def rotateZ(self, angle):
        self.apply_matrix_3x3(Matrix.rotation_z(angle))

    def scale(self, nb):
        self.apply_matrix_3x3(Matrix.id(3) * nb)

    def apply_matrix_3x3(self, mat):
        self.pos = mat * self.pos

    def apply_matrix_4x4(self, mat):
        self.pos = (mat * self.pos.add_dim(1)).remove_dim()


class Point3D(Primitive3D):
    def __init__(self, pos: Vec, color: Vec):
        super().__init__(pos)
        self.color = color

    def to_2d(self, engine, vertices, col_infos):
        vertices.append(self.pos)
        return Point2D(len(vertices)-1, self.color)


class Quad3D(Primitive3D):
    def __init__(self, v1, v2, v3, v4, color):
        pos = (v1 + v2 + v3 + v4) / 4
        super().__init__(pos, max(dist(pos, v1), dist(pos, v2), dist(pos, v3), dist(pos, v4)))
        self.corners = [v1, v2, v3, v4]
        self.color = color

    def to_2d(self, engine, vertices, col_infos):
        for corner in self.corners:
            vertices.append(corner)
        col_infos.append((self.pos, cross(self.corners[0] - self.corners[1],
                                          self.corners[0] - self.corners[2]),
                          self.color))
        return Quad2D(len(vertices)-4, len(vertices)-3, len(vertices)-2, len(vertices)-1,
                      len(col_infos)-1)

    def translate(self, vec):
        super().translate(vec)
        for i in range(len(self.corners)):
            self.corners[i] += vec

    def apply_matrix_3x3(self, mat):
        super().apply_matrix_3x3(mat)
        for i in range(len(self.corners)):
            self.corners[i] = mat * self.corners[i]

    def apply_matrix_4x4(self, mat):
        super().apply_matrix_4x4(mat)
        for i in range(len(self.corners)):
            self.corners[i] = (mat * self.corners[i].add_dim(1)).remove_dim()


class Model3D(Primitive3D):
    def __init__(self):
        super().__init__(Vec(0, 0, 0))
        self.primitives: list[Primitive3D] = []
        self.finalized = False

    def add(self, primitive: Primitive3D):
        self.finalized = False
        self.primitives.append(primitive)

    def finalize(self):
        if self.finalized:
            return
        self.finalized = True
        for primitive in self.primitives:
            primitive.finalize()
        for primitive in self.primitives:
            self.pos += primitive.pos
        self.pos /= max(len(self.primitives), 1)
        for primitive in self.primitives:
            d = dist(self.pos, primitive.pos) + primitive.size
            if d > self.size:
                self.size = d

    def to_2d(self, engine, vertices, col_infos):
        assert self.finalized, "Il faut appeler la methode finalize() avant de dessiner le modèle"
        res = Container()
        for primitive in self.primitives:
            res.add(primitive.to_2d(engine, vertices, col_infos))
        return res

    def split(self):
        return self.primitives

    def splittable(self):
        return True

    def translate(self, vec):
        super().translate(vec)
        for p in self.primitives:
            p.translate(vec)

    def apply_matrix_3x3(self, mat):
        super().apply_matrix_3x3(mat)
        for p in self.primitives:
            p.apply_matrix_3x3(mat)

    def apply_matrix_4x4(self, mat):
        super().apply_matrix_4x4(mat)
        for p in self.primitives:
            p.apply_matrix_4x4(mat)
