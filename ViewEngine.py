from Matrix import *
from Light import *
from GraphicPrimitives import *


class Point3D:
    def __init__(self, pos: Vec, color: Vec):
        self.pos = pos
        self.color = color

    def to_2d(self, engine):
        return Point2D(engine.to_screen(self.pos), self.color)


class Quad3D:
    def __init__(self, v1, v2, v3, v4, color):
        self.pos = (v1 + v2 + v3 + v4) / 4
        self.corners = v1, v2, v3, v4
        self.color = color

    def to_2d(self, engine):
        return Quad2D(engine.to_screen(self.corners[0]),
                      engine.to_screen(self.corners[1]),
                      engine.to_screen(self.corners[2]),
                      engine.to_screen(self.corners[3]),
                      engine.color(self.pos, cross(self.corners[0] - self.corners[1], self.corners[0] - self.corners[2]), self.color))


def point_3d(vec, color=Vec(255, 255, 255)):
    return Point3D(vec, color)


def quad_3d(v1, v2, v3, v4, color=Vec(255, 255, 255)):
    return Quad3D(v1, v2, v3, v4, color)


def quad_hor_3d(a, b, h=None, color=Vec(255, 255, 255)):
    """ v1 and v2 must be of dimension 3 or parameter h filled
    If v1 and v2 have different z, the program will take the v1's z
    """
    assert a.dim() == 2 or h is not None, "v1 must be of dimension 3, or the parameter h must be filled"
    if h is None:
        h = a.z
    v1 = a.add_dim() + Vec(0, 0, h)
    v2 = Vec(b.x, a.y, h)
    v3 = b.add_dim() + Vec(0, 0, h)
    v4 = Vec(a.x, b.y, h)
    return quad_3d(v1, v2, v3, v4, color)


def quad_vert_3d(a, b, color=Vec(255, 255, 255)):
    """ v1 and v2 must be of dimension 3 """
    v1 = a
    v2 = Vec(a.x, a.y, b.z)
    v3 = b
    v4 = Vec(b.x, b.y, a.z)
    return quad_3d(v1, v2, v3, v4, color)


class ViewEngine:
    base_matrix = Matrix.rotation_z(pi / 4) * Matrix.rotation_x(pi / 4)

    def __init__(self, screen: pg.Surface):
        self.base = [0, 0, 0]
        self.base[0] = self.base_matrix * Vec(1, 0, 0) * 40
        self.base[1] = self.base_matrix * Vec(0, 1, 0) * 40
        self.base[2] = self.base_matrix * Vec(0, 0, 1) * 40
        self.matrix = Matrix(self.base[0], self.base[1], self.base[2]).transpose()
        self.screen_size = Vec(*screen.get_size())
        self.screen = screen

        self.light_direction = Vec(1, 1, 1).normalize()
        self.light_color = Vec(1, 1, 0.9)

        self.lights = []

        self.to_draw_buffer = []

    def change_base(self, matrix):
        self.base_matrix = matrix
        self.base[0] = self.base_matrix * Vec(1, 0, 0) * 40
        self.base[1] = self.base_matrix * Vec(0, 1, 0) * 40
        self.base[2] = self.base_matrix * Vec(0, 0, 1) * 40
        self.matrix = Matrix(self.base[0], self.base[1], ZERO3).transpose()

    def set_light_direction(self, v: Vec):
        assert v.dim() == 3
        self.light_direction = v.normalize()

    def set_light_color(self, col):
        assert col.dim() == 3
        self.light_color = col

    def add_point_light(self, pos, color=Vec(1, 1, 1), power=1):
        self.lights.append(PointLight(pos, color, power))

    def to_screen(self, v):
        return (self.matrix * v).remove_dim() + self.screen_size / 2

    def cam_dist(self, pos):
        return (self.matrix * pos).z



    def color(self, pos, normal, color):
        return self._intensity(pos, normal) * color

    def _intensity(self, pos, normal):
        res = self._radiance(normal) + self._lights(pos, normal)
        return Vec(max(min(res.r, 1), 0), max(0, min(res.g, 1)), max(0, min(res.b, 1)))

    def _radiance(self, normal):
        """ Met la lumière type Soleil
        Attention, elle suppose que regarder une face d'un côté, ou de l'autre ne change rien.
        """
        return abs(dot(normal, self.light_direction)) * self.light_color

    def _lights(self, pos: Vec, normal: Vec):
        normal = normal.normalize()
        if dot(self.base[2], normal) > 0: normal = -normal
        res = Vec(0, 0, 0)
        for light in self.lights:
            res += light.apply(pos, normal)
        return Vec(min(1, res.r), min(1, res.g), min(1, res.b))

    def add_buffer(self, elt):
        key = self.cam_dist(elt.pos)
        self.to_draw_buffer.append((key, elt))

    def draw_buffer(self):
        self.to_draw_buffer.sort(reverse=True, key=lambda e: e[0])
        for _, primitive in self.to_draw_buffer:
            primitive.to_2d(self).draw(self.screen)
        self.to_draw_buffer = []

    def finalize(self):
        self.draw_buffer()


if __name__ == "__main__":
    pass
    # engine = ViewEngine(Vec(1100, 700))
    # print(engine.base)
    # print(engine.to_screen(Vec(2, 2, 2)))
