import maya.cmds as cmds


def calculate_distance_between(from_distance, to_distance):
    distance_between_node = cmds.createNode("distanceBetween", name=f"{from_distance}_{to_distance}_distance_node")
    cmds.connectAttr(f"{from_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix1")
    cmds.connectAttr(f"{to_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix2")

    distance_between_value = cmds.getAttr(f"{distance_between_node}.distance")

    return distance_between_value, distance_between_node


class LegTwist:

    def __init__(self, prefix):
        self.prefix = prefix
        self.leg_segments = [f"{self.prefix}_upperleg", f"{self.prefix}_lowerleg", f"{self.prefix}_ankle"]

    def create_twist_joints(self, base_joint, end_joint):
        twist_a = cmds.duplicate(base_joint, parentOnly=True, name=f"{self.prefix}_leg_twist_a01")[0]
        cmds.setAttr(f"{twist_a}.radius", 5)
        twist_d = cmds.duplicate(end_joint, parentOnly=True, name=f"{self.prefix}_leg_twist_d01")[0]
        cmds.setAttr(f"{twist_d}.radius", 5)
        cmds.joint(twist_d, edit=True, orientJoint="none", zeroScaleOrient=True)
        cmds.parent(twist_d, twist_a)
        return twist_a, twist_d

    def create_twist_joints_hierarchy(self, twist_d, distance_between_value):
        twist_b = cmds.duplicate(twist_d, parentOnly=True, name=f"{self.prefix}_leg_twist_b01")[0]
        twist_c = cmds.duplicate(twist_d, parentOnly=True, name=f"{self.prefix}_leg_twist_c01")[0]
        cmds.move(0, - (distance_between_value * 0.66), 0, twist_b, relative=True, objectSpace=True)
        cmds.move(0, - (distance_between_value * 0.33), 0, twist_c, relative=True, objectSpace=True)
        return twist_b, twist_c

    def create_ik_handle(self, start_joint, end_effector):
        ik_handle = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_{end_effector}",
            startJoint=start_joint,
            endEffector=end_effector,
            solver="ikSCsolver"
        )[0]
        return ik_handle

    def setup_upper_leg(self):
        twist_a, twist_d = self.create_twist_joints(self.leg_segments[0], self.leg_segments[1])
        distance_between_value, _ = calculate_distance_between(twist_a, twist_d)
        twist_b, twist_c = self.create_twist_joints_hierarchy(twist_d, distance_between_value)
        ik_handle_shoulder = self.create_ik_handle(twist_a, twist_d)
        # cmds.parent(ik_handle_shoulder, f"{self.prefix}_clavicle")
        cmds.pointConstraint(self.leg_segments[1], ik_handle_shoulder, maintainOffset=False)
        cmds.orientConstraint(self.leg_segments[0], twist_d, maintainOffset=False)

        b_point = cmds.pointConstraint([twist_a, twist_d], twist_b, maintainOffset=False)[0]
        b_orient = cmds.orientConstraint([twist_a, twist_d], twist_b, maintainOffset=False)[0]
        cmds.setAttr(f"{b_point}.{twist_a}W0", 2)
        cmds.setAttr(f"{b_orient}.{twist_a}W0", 2)

        c_point = cmds.pointConstraint([twist_a, twist_d], twist_c, maintainOffset=False)[0]
        c_orient = cmds.orientConstraint([twist_a, twist_d], twist_c, maintainOffset=False)[0]
        cmds.setAttr(f"{c_point}.{twist_d}W1", 2)
        cmds.setAttr(f"{c_orient}.{twist_d}W1", 2)

    def setup_lower_leg(self):
        twist_a, twist_d = self.create_twist_joints(self.leg_segments[-1], self.leg_segments[1])
        distance_between_value, _ = calculate_distance_between(twist_a, twist_d)
        twist_b, twist_c = self.create_twist_joints_hierarchy(twist_d, distance_between_value)
        ik_handle_wrist = self.create_ik_handle(twist_a, twist_d)
        cmds.parent(ik_handle_wrist, self.leg_segments[-1])
        cmds.pointConstraint(self.leg_segments[1], ik_handle_wrist, maintainOffset=False)
        cmds.orientConstraint(self.leg_segments[1], twist_d, maintainOffset=False)

        b_point = cmds.pointConstraint([twist_a, twist_d], twist_b, maintainOffset=False)[0]
        b_orient = cmds.orientConstraint([twist_a, twist_d], twist_b, maintainOffset=False)[0]
        cmds.setAttr(f"{b_point}.{twist_a}W0", 2)
        cmds.setAttr(f"{b_orient}.{twist_a}W0", 2)

        c_point = cmds.pointConstraint([twist_a, twist_d], twist_c, maintainOffset=False)[0]
        c_orient = cmds.orientConstraint([twist_a, twist_d], twist_c, maintainOffset=False)[0]
        cmds.setAttr(f"{c_point}.{twist_d}W1", 2)
        cmds.setAttr(f"{c_orient}.{twist_d}W1", 2)

    def create_leg_twist(self):
        self.setup_upper_leg()
        self.setup_lower_leg()
