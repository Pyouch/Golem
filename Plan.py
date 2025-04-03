from Vec import Vec, dot


class Plan:
    def __init__(self, point: Vec, normal: Vec):
        self.point = self.abs_point = point
        self.normal = self.abs_normal = normal.normalize()

    def in_normal_dir(self, point: Vec, tolerance=0) -> int:
        """
        The plan cuts the space in two sides. This function returns if the point is in
        the side pointed by the normal vector
        -1 if it is behind the plan
        0 if it is a bit in front, and a bit behind
        1 if it is completely in front.
        :param point: the point checked
        :param tolerance: if he permits the point to be a bit outside
        """
        r = dot(point - self.point, self.normal)  # Distance entre le point et le plan
        if r > tolerance:
            return 1
        elif r > -tolerance:
            return 0
        else:
            return -1

    def __str__(self):
        return f"Plan<{self.point}, {self.normal}>"

    def apply_matrix(self, mat, inverse_t_mat):
        self.point = (mat * self.abs_point.add_dim(1)).remove_dim()
        self.normal = (inverse_t_mat * self.abs_normal.add_dim(0)).remove_dim()
