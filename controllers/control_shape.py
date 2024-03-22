import maya.cmds as cmds


class ControlShape:
    CURVE_ARROW_POINTS = [
        (1, 0, -1),
        (1, 0, -2),
        (3, 0, 0),
        (1, 0, 2),
        (1, 0, 1),
        (-3, 0, 1),
        (-3, 0, -1),
        (1, 0, -1),
    ]

    CURVE_DOUBLE_ARROW_POINTS = [
        (1, 0, -1),
        (1, 0, -2),
        (3, 0, 0),
        (1, 0, 2),
        (1, 0, 1),
        (-1, 0, 1),
        (-1, 0, 2),
        (-3, 0, 0),
        (-1, 0, -2),
        (-1, 0, -1),
        (1, 0, -1),
    ]

    CURVE_COG_POINTS = [
        (0, 0, -2.5),
        (1, 0, -1.5),
        (0.5, 0, -1.5),
        # (0.5, 0, -0.5),
        (1.5, 0, -0.5),
        (1.5, 0, -1),
        (2.5, 0, 0),
        (1.5, 0, 1),
        (1.5, 0, 0.5),
        # (0.5, 0, 0.5),
        (0.5, 0, 1.5),
        (1, 0, 1.5),
        (0, 0, 2.5),
        (-1, 0, 1.5),  # reversed
        (-0.5, 0, 1.5),
        # (-0.5, 0, 0.5),
        (-1.5, 0, 0.5),
        (-1.5, 0, 1),
        (-2.5, 0, 0),
        (-1.5, 0, -1),
        (-1.5, 0, -0.5),
        # (-0.5, 0, -0.5),
        (-0.5, 0, -1.5),
        (-1, 0, -1.5),
        (0, 0, -2.5),
    ]

    CURVE_WRIST_POINTS = [
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
        (-1, 0, 1.5),  # reversed
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

    CURVE_LOLLY_POINTS = [
        (0, 0, 0),
        (0, 0, -2),
        (-0.5, 0, -2.5),
        (0, 0, -3),
        (0.5, 0, -2.5),
        (0, 0, -2),
    ]

    CURVE_TRIANGLE_POINTS = [
        (0, 0, 3),
        (3, 0, -3),
        (-3, 0, -3),
        (0, 0, 3),
    ]

    def select_control_shape(self, shape, name):
        match shape:
            case "circle":
                return self.curve_circle(name=name)
            case "star":
                return self.curve_star(name=name)
            case _:
                return self.curve_circle(name=name)

    @staticmethod
    def curve_arrow(name):
        curve = cmds.curve(
            point=ControlShape.CURVE_ARROW_POINTS,
            degree=1,
            name=name,
        )

        cmds.scale(10, 10, 10, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_double_arrow(name):
        curve = cmds.curve(
            point=ControlShape.CURVE_DOUBLE_ARROW_POINTS,
            degree=1,
            name=name,
        )

        cmds.scale(10, 10, 10, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_cog(name):
        curve = cmds.curve(
            point=ControlShape.CURVE_COG_POINTS,
            degree=1,
            name=name,
        )

        cmds.scale(20, 20, 20, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_wrist(name):
        curve = cmds.curve(point=ControlShape.CURVE_WRIST_POINTS, degree=1, name=name)

        cmds.scale(10, 10, 10, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_circle(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=12, degree=1, sections=32, name=name)

        # cmds.scale(curve, [1, 1, 1])
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve[0]

    @staticmethod
    def curve_star(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=12, degree=1, sections=32, name=name)
        control_vertices = cmds.ls(f"{name}.cv[0:]", flatten=True)
        for i, vertex in enumerate(control_vertices):
            if not (i % 2) == 0:
                cmds.select(vertex)
                cmds.scale(0.75, 0.75, 0.75, vertex)

        return curve[0]

    @staticmethod
    def curve_head(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), sections=8, name=name)
        vertices_to_move = [f"{name}.cv[3]", f"{name}.cv[7]"]
        cmds.select(vertices_to_move)
        cmds.move(0, 0.25, 0, relative=True)

        cmds.rotate(90, 0, 0, curve)
        cmds.scale(10, 10, 10, curve)
        cmds.makeIdentity(curve, apply=True, rotate=True, scale=True)

        return curve

    @staticmethod
    def curve_lolly(name):
        curve = cmds.curve(point=ControlShape.CURVE_LOLLY_POINTS, degree=1, name=name)

        cmds.scale(2, 2, 2, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_triangle(name):
        curve = cmds.curve(point=ControlShape.CURVE_TRIANGLE_POINTS, degree=1, name=name)

        cmds.scale(2, 2, 2, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_text(name, text):
        curve = cmds.textCurves(name=name, font="Times-Roman", text=text)[0]

        cmds.xform(curve, centerPivots=True)
        cmds.scale(25, 25, 25, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_jaw(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), sections=8, name=name)
        vertices_to_move = [f"{name}.cv[3]", f"{name}.cv[7]"]
        vertices_to_scale = [f"{name}.cv[1]", f"{name}.cv[5]"]

        cmds.select(vertices_to_move)
        cmds.move(0, 1, 0, relative=True)
        cmds.scale(1.25, 1, 0, relative=True)

        cmds.select(vertices_to_scale)
        cmds.scale(0, 0, 0.75, relative=True)

        cmds.scale(10, 10, 10, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_waist(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), sections=8, name=name)
        vertices_to_move = [f"{name}.cv[1]", f"{name}.cv[5]"]
        cmds.select(vertices_to_move)
        cmds.move(0, -0.5, 0, relative=True)

        cmds.scale(25, 25, 25, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_hip(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), sections=8, name=name)
        vertices_to_move = [f"{name}.cv[1]", f"{name}.cv[5]"]
        cmds.select(vertices_to_move)
        cmds.move(0, 0.25, 0, relative=True)

        cmds.scale(25, 25, 25, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_pelvis(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), sections=8, name=name)
        vertices_to_move = [f"{name}.cv[1]", f"{name}.cv[5]"]
        cmds.select(vertices_to_move)
        cmds.move(0, -0.25, 0, relative=True)

        cmds.scale(25, 25, 25, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

    @staticmethod
    def curve_shoulder(name):
        curve = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), sections=8, name=name)
        vertices_to_move = [f"{name}.cv[1]", f"{name}.cv[5]"]
        cmds.select(vertices_to_move)
        cmds.move(0, -0.5, 0, relative=True)

        cmds.scale(25, 25, 25, curve)
        cmds.makeIdentity(curve, apply=True, scale=True)

        return curve

if __name__ == "__main__":
    pass
