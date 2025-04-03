import Matrix

import Light
from Light import *
from Matrix import *
from Model3D import *
from Plan import *


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
    TILE_SIZE = 40

    def __init__(self, screen: pg.Surface):
        self.base: list[Vec] = [
            self.base_matrix * Vec(1, 0, 0) * self.TILE_SIZE,
            self.base_matrix * Vec(0, 1, 0) * self.TILE_SIZE,
            self.base_matrix * Vec(0, 0, 1) * self.TILE_SIZE
        ]
        self.screen_size: Vec = Vec(*screen.get_size())
        self.projection_matrix: Matrix = Matrix(self.base[0]["xyz0"] + Vec(0, 0, 0, self.screen_size.x / 2),
                                                self.base[1]["xyz0"] + Vec(0, 0, 0, self.screen_size.y / 2),
                                                self.base[2]["xyz0"],
                                                Vec(0, 0, 0, 1)).transpose()
        self.cam_matrix = Matrix(1, 0, 0, 0,
                                 0, 1, 0, 0,
                                 0, 0, 1, 0,
                                 0, 0, 0, 1)
        self.matrix = self.projection_matrix * self.cam_matrix
        self.invert_cam_matrix = self.cam_matrix.invert()
        self.screen: pg.Surface = screen

        self.light_direction: Vec = Vec(1, 1, 1).normalize()
        self.light_color: Vec = Vec(1, 1, 0.9)

        self.lights: list[Light] = []

        self.to_draw_buffer: list[tuple[int, Primitive3D]] = []

        self.vision_delimiter_plans: list[Plan] = [
            Plan(-self.base[0] * self.screen_size[0] / 2 / self.TILE_SIZE ** 2, self.base[0]),
            Plan(self.base[0] * self.screen_size[0] / 2 / self.TILE_SIZE ** 2, -self.base[0]),
            Plan(-self.base[1] * self.screen_size[1] / 2 / self.TILE_SIZE ** 2, self.base[1]),
            Plan(self.base[1] * self.screen_size[1] / 2 / self.TILE_SIZE ** 2, -self.base[1])
        ]

        self.projected_points: dict[Vec, Vec] = {}

    def move(self, x, y, z):
        self.cam_matrix = Matrix.translate(x, y, z) * self.cam_matrix
        self.invert_cam_matrix = self.cam_matrix.invert()
        self.matrix = self.projection_matrix * self.cam_matrix
        for plan in self.vision_delimiter_plans:
            plan.apply_matrix(self.invert_cam_matrix, self.cam_matrix.transpose())

    def set_light_direction(self, v: Vec):
        assert v.dim() == 3
        self.light_direction = v.normalize()

    def set_light_color(self, col):
        assert col.dim() == 3
        self.light_color = col

    def add_point_light(self, pos, color=Vec(1, 1, 1), power=1):
        self.lights.append(PointLight(pos, color, power))

    def to_screen(self, v):
        if v in self.projected_points:
            return self.projected_points[v]
        else:
            p = (self.matrix * v.add_dim(1)).remove_dim(2)
            self.projected_points[v] = p
            return p

    def cam_dist(self, pos):
        return dot(pos, self.base[2])

    def color(self, pos, normal, color):
        return self._intensity(pos, normal) * color

    def _intensity(self, pos: Vec, normal: Vec) -> Vec:
        res = self._radiance(normal) + self._lights(pos, normal)
        return Vec(max(min(res.r, 1), 0), max(0, min(res.g, 1)), max(0, min(res.b, 1)))

    def _radiance(self, normal):
        """ It puts some light if it's in the direction of the light_direction
        It supposes that if we look it from behind or from front, it doesn't change anything.
        """
        return abs(dot(normal, self.light_direction)) * self.light_color

    def _lights(self, pos: Vec, normal: Vec):
        normal = normal.normalize()
        if dot(self.base[2], normal) > 0: normal = -normal
        res = Vec(0, 0, 0)
        for light in self.lights:
            res += light.apply(pos, normal)
        return Vec(min(1, res.r), min(1, res.g), min(1, res.b))

    def add_buffer(self, elt: Primitive3D) -> bool:
        """
        Ajoute dans le buffer la primitive 3D.
        :return: Si elle a été ajoutée ou pas (Peut ne pas être ajoutée si la
        primitive n'est pas visible)
        """
        min_p = 1
        for plan in self.vision_delimiter_plans:
            p = plan.in_normal_dir(elt.pos, elt.size)
            if p == -1:
                return False
            elif p == 0:
                min_p = 0
        if min_p == 0 and elt.splittable():
            for e in elt.split():
                self.add_buffer(e)
            return True
        key = self.cam_dist(elt.pos)
        self.to_draw_buffer.append((key, elt))
        return True

    def draw_buffer(self):
        self.to_draw_buffer.sort(reverse=True, key=lambda e: e[0])
        for _, primitive in self.to_draw_buffer:
            primitive.to_2d(self).draw(self.screen)
        self.to_draw_buffer = []

    def finalize(self):
        self.draw_buffer()
        self.projected_points = {}
        # TODO: clear les projected_points lorsqu'on modifie la caméra


if __name__ == "__main__":
    pass
    # engine = ViewEngine(Vec(1100, 700))
    # print(engine.base)
    # print(engine.to_screen(Vec(2, 2, 2)))
