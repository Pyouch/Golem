from Vec import Vec, dot


class Plan:
    def __init__(self, point: Vec, normal: Vec):
        self.point = point
        self.normal = normal.normalize()

    def in_normal_dir(self, point: Vec, tolerance=0):
        """
        The plan cuts the space in two sides. This function returns if the point is in
        the side pointed by the normal vector
        :param point: the point checked
        :param tolerance: if he permits the point to be a bit outside
        """
        return dot(point - self.point + tolerance * self.normal, self.normal) > 0

    def __str__(self):
        return f"Plan<{self.point}, {self.normal}>"

