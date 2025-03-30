from GraphicPrimitives import *


class Primitive3D:
    def __init__(self, pos: Vec, size: int = 0):
        """
        :param pos: The position of the middle of the primitive
        :param size: The distance between the position and the most far point of
        the primitive.
        """
        self.pos = pos
        self.size = size

    def to_2d(self, engine) -> Primitive2D:
        pass

    def split(self):
        return []

    def splittable(self):
        return False

    def finalize(self):
        pass


class Point3D(Primitive3D):
    def __init__(self, pos: Vec, color: Vec):
        super().__init__(pos)
        self.color = color

    def to_2d(self, engine):
        return Point2D(engine.to_screen(self.pos), self.color)


class Quad3D(Primitive3D):
    def __init__(self, v1, v2, v3, v4, color):
        pos = (v1 + v2 + v3 + v4) / 4
        super().__init__(pos, max(dist(pos, v1), dist(pos, v2), dist(pos, v3), dist(pos, v4)))
        self.corners = v1, v2, v3, v4
        self.color = color

    def to_2d(self, engine):
        return Quad2D(engine.to_screen(self.corners[0]),
                      engine.to_screen(self.corners[1]),
                      engine.to_screen(self.corners[2]),
                      engine.to_screen(self.corners[3]),
                      engine.color(self.pos, cross(self.corners[0] - self.corners[1],
                                                   self.corners[0] - self.corners[2]),
                                   self.color))


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

    def to_2d(self, engine):
        assert self.finalized, "Il faut appeler la methode finalize() avant de dessiner le modèle"
        res = Container()
        for primitive in self.primitives:
            res.add(primitive.to_2d(engine))
        return res

    def split(self):
        return self.primitives

    def splittable(self):
        return True
