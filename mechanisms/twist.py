import maya.cmds as cmds


def calculate_distance_between(from_distance: str, to_distance: str) -> tuple[float, str]:
    distance_between_node: str = cmds.createNode("distanceBetween", name=f"{from_distance}_{to_distance}_distance_node")
    cmds.connectAttr(f"{from_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix1")
    cmds.connectAttr(f"{to_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix2")

    distance_between_value: float = cmds.getAttr(f"{distance_between_node}.distance")

    return distance_between_value, distance_between_node


class Twist:

    def __init__(self, prefix: str, name: str, segments: list[str]):
        self.prefix = prefix
        self.name = name
        self.segments = segments

    def create_twist_joints(self, base_joint: str, end_joint: str) -> tuple[str, str]:
        twist_a: str = cmds.duplicate(base_joint, parentOnly=True, name=f"{self.prefix}_{self.name}_twist_a01")[0]
        cmds.setAttr(f"{twist_a}.radius", 5)
        twist_d: str = cmds.duplicate(end_joint, parentOnly=True, name=f"{self.prefix}_{self.name}_twist_d01")[0]
        cmds.setAttr(f"{twist_d}.radius", 5)
        cmds.joint(twist_d, edit=True, orientJoint="none", zeroScaleOrient=True)
        cmds.parent(twist_d, twist_a)
        return twist_a, twist_d

    def create_twist_joints_hierarchy(self, twist_d: str, distance_between_value: float) -> tuple[str, str]:
        twist_b: str = cmds.duplicate(twist_d, parentOnly=True, name=f"{self.prefix}_{self.name}_twist_b01")[0]
        twist_c: str = cmds.duplicate(twist_d, parentOnly=True, name=f"{self.prefix}_{self.name}_twist_c01")[0]
        cmds.move(0, - (distance_between_value * 0.66), 0, twist_b, relative=True, objectSpace=True)
        cmds.move(0, - (distance_between_value * 0.33), 0, twist_c, relative=True, objectSpace=True)
        return twist_b, twist_c

    def create_ik_handle(self, start_joint, end_effector) -> str:
        ik_handle: str = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_{end_effector}",
            startJoint=start_joint,
            endEffector=end_effector,
            solver="ikSCsolver"
        )[0]
        return ik_handle

    @staticmethod
    def create_twist_joints_constraint(twist_a: str, twist_b: str, twist_c: str, twist_d: str) -> None:
        b_point: str = cmds.pointConstraint([twist_a, twist_d], twist_b, maintainOffset=False)[0]
        b_orient: str = cmds.orientConstraint([twist_a, twist_d], twist_b, maintainOffset=False)[0]
        cmds.setAttr(f"{b_point}.{twist_a}W0", 2)
        cmds.setAttr(f"{b_orient}.{twist_a}W0", 2)

        c_point: str = cmds.pointConstraint([twist_a, twist_d], twist_c, maintainOffset=False)[0]
        c_orient: str = cmds.orientConstraint([twist_a, twist_d], twist_c, maintainOffset=False)[0]
        cmds.setAttr(f"{c_point}.{twist_d}W1", 2)
        cmds.setAttr(f"{c_orient}.{twist_d}W1", 2)

    def setup_upper(self) -> None:
        twist_a, twist_d = self.create_twist_joints(self.segments[0], self.segments[1])
        distance_between_value, _ = calculate_distance_between(twist_a, twist_d)
        twist_b, twist_c = self.create_twist_joints_hierarchy(twist_d, distance_between_value)
        ik_handle_upper: str = self.create_ik_handle(twist_a, twist_d)
        # cmds.parent(ik_handle_shoulder, f"{self.prefix}_clavicle")
        cmds.pointConstraint(self.segments[1], ik_handle_upper, maintainOffset=False)
        cmds.orientConstraint(self.segments[0], twist_d, maintainOffset=False)

        self.create_twist_joints_constraint(twist_a=twist_a, twist_b=twist_b, twist_c=twist_c, twist_d=twist_d)

    def setup_lower(self) -> None:
        twist_a, twist_d = self.create_twist_joints(self.segments[-1], self.segments[1])
        distance_between_value, _ = calculate_distance_between(twist_a, twist_d)
        twist_b, twist_c = self.create_twist_joints_hierarchy(twist_d, distance_between_value)
        ik_handle_lower: str = self.create_ik_handle(twist_a, twist_d)
        cmds.parent(ik_handle_lower, self.segments[-1])
        cmds.pointConstraint(self.segments[1], ik_handle_lower, maintainOffset=False)
        cmds.orientConstraint(self.segments[1], twist_d, maintainOffset=False)

        self.create_twist_joints_constraint(twist_a=twist_a, twist_b=twist_b, twist_c=twist_c, twist_d=twist_d)

    def create_twist(self) -> None:
        self.setup_upper()
        self.setup_lower()
