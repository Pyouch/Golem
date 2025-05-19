from Vec import *


class Lighting:
    def __init__(self, light_dir: Vec, light_col: Vec, z_axis: Vec):
        self.light_direction = light_dir
        self.light_color = light_col
        self.z_axis = z_axis

    def lighting(self, col_infos, lights) -> list[Vec]:
        res = []
        for col_info in col_infos:
            res.append(self.color(*col_info, lights))
        return res

    def color(self, pos, normal, color, lights):
        return self._intensity(pos, normal, lights) * color

    def _intensity(self, pos: Vec, normal: Vec, lights) -> Vec:
        res = self._radiance(normal) + self._lights(pos, normal, lights)
        return Vec(max(min(res.r, 1), 0), max(0, min(res.g, 1)), max(0, min(res.b, 1)))

    def _radiance(self, normal):
        """ It puts some light if it's in the direction of the light_direction
        It supposes that if we look it from behind or from front, it doesn't change anything.
        """
        return 0.1 * abs(dot(normal, self.light_direction)) * self.light_color

    def _lights(self, pos: Vec, normal: Vec, lights):
        normal = normal.normalize()
        if dot(self.z_axis, normal) > 0: normal = -normal
        res = Vec(0, 0, 0)
        for light in lights:
            res += light.apply(pos, normal)
        return Vec(min(1, res.r), min(1, res.g), min(1, res.b))
