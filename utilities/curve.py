import maya.cmds as cmds
from utilities.enums import Shape


def select_curve(shape, name, scale):
    match shape:
        case Shape.CIRCLE:
            return curve_circle(name=name, scale=scale)
        case Shape.SQUARE:
            return curve_square(name=name, scale=scale)
        case Shape.TRIANGLE:
            return curve_triangle(name=name, scale=scale)
        case Shape.CUBE:
            return curve_cube(name=name, scale=scale)
        case Shape.FOURWAYARROW:
            return curve_four_way_arrow(name=name, scale=scale)
        case _:
            return curve_circle(name=name, scale=scale)


def curve_circle(name, scale):
    curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=scale, degree=1, sections=32, name=name)

    return curve[0]


def curve_square(name, scale):
    points = [
        (1, 0, 1),
        (1, 0, -1),
        (-1, 0, -1),
        (-1, 0, 1),
        (1, 0, 1),
    ]

    curve = cmds.curve(
        point=points,
        degree=1,
        name=name,
    )

    if name[0] == "R":
        cmds.rotate(0, 180, 0, curve)
    cmds.scale(scale, scale, scale, curve)
    cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

    return curve


def curve_triangle(name, scale):
    points = [
        (0, 0, 1),
        (1, 0, -1),
        (-1, 0, -1),
        (0, 0, 1),
    ]

    curve = cmds.curve(
        point=points,
        degree=1,
        name=name,
    )

    if name[0] == "R":
        cmds.rotate(0, 180, 0, curve)
    cmds.scale(scale, scale, scale, curve)
    cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

    return curve


def curve_cube(name, scale):
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

    curve = cmds.curve(
        point=points,
        degree=1,
        name=name,
    )

    if name[0] == "R":
        cmds.rotate(0, 180, 0, curve)
    cmds.scale(scale, scale, scale, curve)
    cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

    return curve


def curve_four_way_arrow(name, scale):
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

    curve = cmds.curve(
        point=points,
        degree=1,
        name=name,
    )

    if name[0] == "R":
        cmds.rotate(0, 180, 0, curve)
    cmds.scale(scale, scale, scale, curve)
    cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

    return curve


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

    def get_control_shape(self, shape, name, scale):
        match shape:
            case Shape.CIRCLE:
                return self.curve_circle(name=name, scale=scale)
            case Shape.SQUARE:
                return self.curve_square(name=name, scale=scale)
            case Shape.TRIANGLE:
                return self.curve_triangle(name=name, scale=scale)
            case Shape.CUBE:
                return self.curve_cube(name=name, scale=scale)
            case _:
                pass

    @staticmethod
    def get_curve_cv_coordinates(curve):
        control_vertices = cmds.ls(f"{curve}.cv[0:]", flatten=True)
        for vertex in control_vertices:
            positions = cmds.xform(vertex, query=True, translation=True, worldSpace=True)
            cv_positions = (positions[0], positions[1], positions[2])
            print(cv_positions)

    @staticmethod
    def create_curve(name, points, scale=(0.5, 0.5, 0.5)):
        curve = cmds.curve(
            point=points,
            degree=1,
            name=name,
        )

        if name[0] == "R":
            cmds.rotate(0, 180, 0, curve)
        cmds.scale(*scale, curve)
        cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

        return curve


    def curve_circle(self, name, scale):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=scale, degree=1, sections=32, name=name)

        # cmds.scale(2, 2, 2, curve)
        # cmds.makeIdentity(curve, apply=True, scale=True)

        return curve[0]

    def curve_square(self, name, scale):
        points = [
            (1, 0, 1),
            (1, 0, -1),
            (-1, 0, -1),
            (-1, 0, 1),
            (1, 0, 1),
        ]

        curve = cmds.curve(
            point=points,
            degree=1,
            name=name,
        )

        if name[0] == "R":
            cmds.rotate(0, 180, 0, curve)
        cmds.scale(scale, scale, scale, curve)
        cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

        return curve

    def curve_triangle(self, name, scale):
        points = [
            (0, 0, 1),
            (1, 0, -1),
            (-1, 0, -1),
            (0, 0, 1),
        ]

        curve = cmds.curve(
            point=points,
            degree=1,
            name=name,
        )

        if name[0] == "R":
            cmds.rotate(0, 180, 0, curve)
        cmds.scale(scale, scale, scale, curve)
        cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

        return curve

        # return self.create_curve(name, points)

    def curve_cube(self, name, scale):
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

        curve = cmds.curve(
            point=points,
            degree=1,
            name=name,
        )

        if name[0] == "R":
            cmds.rotate(0, 180, 0, curve)
        cmds.scale(scale, scale, scale, curve)
        cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

        return curve
        # return self.create_curve(name, points, scale=(1,1,1))

    @staticmethod
    def curve_text(name, text):
        curve = cmds.textCurves(name=name, font="Times-Roman", text=text)[0]
        cmds.setAttr(f"{curve}.overrideEnabled", True)
        cmds.setAttr(f"{curve}.overrideDisplayType", 2)

        cmds.xform(curve, centerPivots=True)
        cmds.scale(10, 10, 10, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    def curve_chest(self, name):
        points = [
            (20, 0, 15),
            (20, 0, -20),
            (-20, 0, -20),
            (-20, 0, 15),
            (20, 0, 15),
            (15, 30, 20),

            (15, 40, -20),
            (20, 0, -20),
            (15, 40, -20),

            (-15, 40, -20),
            (-20, 0, -20),
            (-15, 40, -20),

            (-15, 30, 20),
            (-20, 0, 15),
            (-15, 30, 20),

            (15, 30, 20)
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
            (1, 4, 1),

            (1, 4, -1),
            (1, 1, -1),
            (1, 4, -1),

            (-1, 4, -1),
            (-1, 0, -1),
            (-1, 4, -1),

            (-1, 4, 1),
            (-1, 0, 1),
            (-1, 4, 1),

            (1, 4, 1),
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
        # points = [
        #     (0, 0, 0),
        #     (0, 1, 0),
        #     (0.5, 1.25, 0),
        #     (0.0, 1.5, 0),
        #     (-0.5, 1.25, 0),
        #     (0, 1, 0),

            # (0, 0, -2),
            # (-0.5, 0, -2.5),
            # (0, 0, -3),
            # (0.5, 0, -2.5),
            # (0, 0, -2),
        # ]
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

    def curve_four_way_arrow(self, name, scale):
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

        curve = cmds.curve(
            point=points,
            degree=1,
            name=name,
        )

        if name[0] == "R":
            cmds.rotate(0, 180, 0, curve)
        cmds.scale(scale, scale, scale, curve)
        cmds.makeIdentity(curve, apply=True, scale=True, rotate=True)

        return curve

        # return self.create_curve(name, points)


    def create_finger_curve(self, name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=8, degree=3, sections=16, name=name)[0]
        selection = cmds.select(f"{curve}.cv[1]", f"{curve}.cv[9]")
        cmds.move(0, 2, 0, selection, relative=True, objectSpace=True)
        cmds.scale(0.25, 0.25, 0.25, curve)
        cmds.makeIdentity(apply=True, scale=True)

        return curve

    def create_joint_curve(self, curve_points):
        curve = cmds.curve(name="curve", point=curve_points, degree=1)
        self.enable_rgb_override(node=curve, rgb=(1, 0, 0))

        for i, cv in enumerate(cmds.ls(f"{curve}.cv[*]", flatten=True)):
            current_locator = f"{i}_LOC"
            cluster = cmds.cluster(cv, name=current_locator)[1]
            cmds.setAttr(f"{cluster}.visibility", False)
            cmds.parent(cluster, current_locator)

    @staticmethod
    def enable_rgb_override(node: str, rgb: tuple[float, float, float]):
        cmds.setAttr(f"{node}.overrideEnabled", True)
        cmds.setAttr(f"{node}.overrideRGBColors", True)
        cmds.setAttr(f"{node}.overrideColorRGB", *rgb)


if __name__ == "__main__":
    pass


def sum_char(n):
    sum = 0
    for index, item in enumerate(n):
        sum += index
    for index, item in enumerate(n):
        sum += index
