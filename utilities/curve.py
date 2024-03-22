import maya.cmds as cmds


class Curve:
    def select_curve(self, curve, name):
        match curve:
            case "L_upperarm" | "R_upperarm":
                return self.curve_upperarm(name=name)
            case "L_lowerarm" | "R_lowerarm":
                return self.curve_lowerarm(name=name)
            case "L_wrist" | "R_wrist":
                return self.curve_wrist(name=name)
            case "L_upperleg" | "R_upperleg":
                return self.curve_upperarm(name=name)
            case "L_lowerleg" | "R_lowerleg":
                return self.curve_lowerarm(name=name)
            case "L_ankle" | "R_ankle":
                return self.curve_wrist(name=name)

    @staticmethod
    def get_curve_cv_coordinates(curve):
        control_vertices = cmds.ls(f"{curve}.cv[0:]", flatten=True)
        for vertex in control_vertices:
            positions = cmds.xform(vertex, query=True, translation=True, worldSpace=True)
            cv_positions = (positions[0], positions[1], positions[2])
            print(cv_positions)

    @staticmethod
    def create_curve(name, points):
        curve = cmds.curve(
            point=points,
            degree=1,
            name=name,
        )

        if name[0] == "R":
            cmds.rotate(0, 180, 0, curve)
        cmds.scale(10, 10, 10, curve)
        cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

        return curve

    @staticmethod
    def curve_circle(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=12, degree=1, sections=32, name=name)

        cmds.scale(2, 2, 2, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve[0]

    def curve_triangle(self, name):
        points = [
            (0, 0, 1),
            (1, 0, -1),
            (-1, 0, -1),
            (0, 0, 1),
        ]
        return self.create_curve(name, points)

    def curve_cube(self, name):
        points = [
            (1, -1, 1),
            (1, -1, -1),
            (-1, -1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),

            (1, 1, -1),
            (1, -1, -1),
            (1, 1, -1),

            (-1, 1, -1),
            (-1, -1, -1),
            (-1, 1, -1),

            (-1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1),

            (1, 1, 1),
        ]
        return self.create_curve(name, points)

    @staticmethod
    def curve_text(name, text):
        curve = cmds.textCurves(name=name, font="Times-Roman", text=text)[0]

        cmds.xform(curve, centerPivots=True)
        cmds.scale(25, 25, 25, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    def curve_chest(self, name):
        points = [
            (10, 0, 7.5),
            (10, 0, -10),
            (-10, 0, -10),
            (-10, 0, 7.5),
            (10, 0, 7.5),
            (7.5, 15, 10),

            (7.5, 20, -10),
            (10, 0, -10),
            (7.5, 20, -10),

            (-7.5, 20, -10),
            (-10, 0, -10),
            (-7.5, 20, -10),

            (-7.5, 15, 10),
            (-10, 0, 7.5),
            (-7.5, 15, 10),

            (7.5, 15, 10),
        ]

        curve = cmds.curve(
            point=points,
            degree=1,
            name=name,
        )

        cmds.scale(1, 1, 1, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)
        cmds.xform(curve, centerPivots=True)

        return curve

    def curve_upperarm(self, name):
        points = [
            (1, 1, 1),
            (1, 1, -1),
            (-1, 0, -1),
            (-1, 0, 1),
            (1, 1, 1),
            (1, 3, 1),

            (1, 3, -1),
            (1, 1, -1),
            (1, 3, -1),

            (-1, 3, -1),
            (-1, 0, -1),
            (-1, 3, -1),

            (-1, 3, 1),
            (-1, 0, 1),
            (-1, 3, 1),

            (1, 3, 1),
        ]
        return self.create_curve(name, points)

    def curve_lowerarm(self, name):
        points = [
            (1, 0, 1),
            (1, 0, -1),
            (-1, 0, -1),
            (-1, 0, 1),
            (1, 0, 1),
            (1, 3, 1),

            (1, 3, -1),
            (1, 0, -1),
            (1, 3, -1),

            (-1, 3, -1),
            (-1, 0, -1),
            (-1, 3, -1),

            (-1, 3, 1),
            (-1, 0, 1),
            (-1, 3, 1),

            (1, 3, 1),
        ]
        return self.create_curve(name, points)

    def curve_wrist(self, name):
        points = [
            (1, 0, 1),
            (1, 0, -1),
            (-1, 0, -1),
            (-1, 0, 1),
            (1, 0, 1),
            (1, 3, 1),

            (1, 3, -1),
            (1, 0, -1),
            (1, 3, -1),

            (-0.5, 2, -1),
            (-1, 0, -1),
            (-0.5, 2, -1),

            (-0.5, 2, 1),
            (-1, 0, 1),
            (-0.5, 2, 1),

            (1, 3, 1),
        ]

        return self.create_curve(name, points)

    def curve_finger(self, name):
        points = [
            (0, 0, 0),
            (0, 0, -2),
            (-0.5, 0, -2.5),
            (0, 0, -3),
            (0.5, 0, -2.5),
            (0, 0, -2),
        ]

        return self.create_curve(name, points)

    def curve_one_way_arrow(self, name):
        points = [
            (1.5, 0, -0.5),
            (1.5, 0, -1),
            (2.5, 0, 0),
            (1.5, 0, 1),
            (1.5, 0, 0.5),
            (-2.5, 0, 0.5),
            (-2.5, 0, -0.5),
            (1.5, 0, -0.5),
        ]

        return self.create_curve(name, points)

    def curve_two_way_arrow(self, name):
        points = [
            (0, 0, -0.5),
            (1.5, 0, -0.5),
            (1.5, 0, -1),
            (2.5, 0, 0),
            (1.5, 0, 1),
            (1.5, 0, 0.5),
            (0, 0, 0.5),    # reversed
            (-1.5, 0, 0.5),
            (-1.5, 0, 1),
            (-2.5, 0, 0),
            (-1.5, 0, -1),
            (-1.5, 0, -0.5),
            (0, 0, -0.5),
        ]

        return self.create_curve(name, points)

    def curve_three_way_arrow(self, name):
        points = [
            (0, 0, -0.5),
            (1.5, 0, -0.5),
            (1.5, 0, -1),
            (2.5, 0, 0),
            (1.5, 0, 1),
            (1.5, 0, 0.5),
            (0.5, 0, 0.5),
            (0.5, 0, 1.5),
            (1, 0, 1.5),
            (0, 0, 2.5),
            (-1, 0, 1.5),   # reversed
            (-0.5, 0, 1.5),
            (-0.5, 0, 0.5),
            (-1.5, 0, 0.5),
            (-1.5, 0, 1),
            (-2.5, 0, 0),
            (-1.5, 0, -1),
            (-1.5, 0, -0.5),
            (0, 0, -0.5),
        ]

        return self.create_curve(name, points)

    def curve_four_way_arrow(self, name):
        points = [
            (0, 0, -2.5),
            (1, 0, -1.5),
            (0.5, 0, -1.5),
            (0.5, 0, -0.5),
            (1.5, 0, -0.5),
            (1.5, 0, -1),
            (2.5, 0, 0),
            (1.5, 0, 1),
            (1.5, 0, 0.5),
            (0.5, 0, 0.5),
            (0.5, 0, 1.5),
            (1, 0, 1.5),
            (0, 0, 2.5),
            (-1, 0, 1.5),   # reversed
            (-0.5, 0, 1.5),
            (-0.5, 0, 0.5),
            (-1.5, 0, 0.5),
            (-1.5, 0, 1),
            (-2.5, 0, 0),
            (-1.5, 0, -1),
            (-1.5, 0, -0.5),
            (-0.5, 0, -0.5),
            (-0.5, 0, -1.5),
            (-1, 0, -1.5),
            (0, 0, -2.5),
        ]

        return self.create_curve(name, points)


if __name__ == "__main__":
    pass
