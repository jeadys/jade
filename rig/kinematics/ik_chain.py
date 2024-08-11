import maya.cmds as cmds

from data.rig_structure import Segment
from utilities.enums import ForwardAxis, RotateOrder, UpAxis, WorldUpType
from utilities.relations import has_parent
from utilities.shapes import cube_points
from utilities.transforms import bake_transform_to_offset_parent_matrix


class IKChain:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.side = cmds.getAttr(f"{self.node}.side")
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.prefix = f"{self.side}{self.name}_{self.module_nr}"
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def ik_joint(self, segments: list[Segment]) -> list[str]:
        joint_group = f"{self.prefix}_IK_GROUP"
        if not cmds.objExists(joint_group):
            cmds.group(empty=True, name=joint_group)

        joint_layer_group = f"{self.prefix}_LAYER_GROUP"
        if not cmds.objExists(joint_layer_group):
            joint_layer_group = cmds.group(empty=True, name=joint_layer_group)

        if not has_parent(joint_group, joint_layer_group):
            cmds.parent(joint_group, joint_layer_group)

        ik_joints: list[str] = []
        for segment in segments:
            if cmds.objExists(f"{segment}_IK"):
                continue

            current_segment = cmds.duplicate(f"{segment}_JNT", name=f"{segment}_IK", parentOnly=True)[0]
            cmds.parentConstraint(current_segment, f"{segment}_JNT", maintainOffset=True)

            parent_joint = cmds.listRelatives(segment, parent=True, shapes=False, type="transform")
            if parent_joint and cmds.objExists(f"{parent_joint[0]}_IK"):
                cmds.parent(current_segment, f"{parent_joint[0]}_IK")
            else:
                cmds.parent(current_segment, joint_group)

            ik_joints.append(current_segment)

        if self.selection and cmds.objExists(f"{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{self.selection[0]}_JNT", joint_group, maintainOffset=True)
        elif self.selection and not cmds.objExists(f"{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{self.selection[0]}_JNT", joint_group, maintainOffset=True)

        return ik_joints

    def ik_control(self, segments: list[Segment]) -> list[str]:
        control_group = f"{self.prefix}_IK_CTRL_GROUP"
        if not cmds.objExists(control_group):
            cmds.group(empty=True, name=control_group)

        joint_control_group = f"{self.prefix}_CONTROL_GROUP"
        if not cmds.objExists(joint_control_group):
            cmds.group(empty=True, name=joint_control_group)

        if not has_parent(control_group, joint_control_group):
            cmds.parent(control_group, joint_control_group)

        ik_handle = cmds.ikHandle(name=f"{self.prefix}_ikHandle",
                                  startJoint=f"{segments[0]}_IK",
                                  endEffector=f"{segments[-1]}_IK",
                                  solver="ikRPsolver")[0]

        ik_control = cmds.curve(name=f"{self.prefix}_IK_CTRL", pointWeight=cube_points, degree=1)
        cmds.setAttr(f"{ik_control}.rotateOrder", RotateOrder.XYZ)
        cmds.matchTransform(ik_control, f"{segments[-1]}_IK", position=True, rotation=True, scale=False)
        cmds.orientConstraint(ik_control, f"{segments[-1]}_IK", maintainOffset=True)

        cmds.parent(ik_handle, ik_control)

        pole_control = cmds.curve(name=f"{self.prefix}_POLE_CTRL", pointWeight=cube_points, degree=1)
        cmds.setAttr(f"{pole_control}.rotateOrder", RotateOrder.XYZ)
        cmds.matchTransform(pole_control, f"{segments[1]}_IK", position=True, rotation=False, scale=False)
        # cmds.move(0, 0, -20, pole_control, relative=True, objectSpace=True)
        cmds.poleVectorConstraint(pole_control, ik_handle)

        cmds.parent(ik_control, control_group)
        cmds.parent(pole_control, control_group)

        bake_transform_to_offset_parent_matrix(ik_control)
        bake_transform_to_offset_parent_matrix(pole_control)

        # if self.selection and cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
        #     cmds.parentConstraint(f"{self.prefix}{self.selection[0]}_JNT", control_group, maintainOffset=True)
        # elif self.selection and not cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
        #     cmds.parentConstraint(f"{self.selection[0]}_JNT", control_group, maintainOffset=True)

        return [ik_control, pole_control]

    def spline_kinematic(self, segments):
        pelvis_mch = cmds.joint(radius=3, rotationOrder=RotateOrder.YZX.name,
                                name=f"{self.side}pelvis_{self.module_nr}_MCH")
        cmds.matchTransform(pelvis_mch, f"{segments[0]}_JNT", position=True, rotation=False, scale=False)

        back_mch = cmds.joint(radius=3, rotationOrder=RotateOrder.YZX.name,
                              name=f"{self.side}back_{self.module_nr}_MCH")
        cmds.matchTransform(back_mch, f"{segments[len(segments) // 2]}_JNT", position=True, rotation=False, scale=False)
        # We need to get the center between the start/end of the segments when the number of segments is an even number.
        if len(segments) % 2 == 0:
            temp_constraint = cmds.pointConstraint([f"{segments[0]}_JNT", f"{segments[-1]}_JNT"], back_mch,
                                                   maintainOffset=False, skip=["x", "z"])
            cmds.delete(temp_constraint)
        cmds.parent(back_mch, world=True)

        chest_mch = cmds.joint(radius=3, rotationOrder=RotateOrder.YZX.name,
                               name=f"{self.side}chest_{self.module_nr}_MCH")
        cmds.matchTransform(chest_mch, f"{segments[-1]}_JNT", position=True, rotation=False, scale=False)
        cmds.parent(chest_mch, world=True)

        cmds.setAttr(f"{pelvis_mch}.radius", 5)
        bake_transform_to_offset_parent_matrix(pelvis_mch)

        cmds.setAttr(f"{back_mch}.radius", 5)
        bake_transform_to_offset_parent_matrix(back_mch)

        cmds.setAttr(f"{chest_mch}.radius", 5)
        bake_transform_to_offset_parent_matrix(chest_mch)

        pelvis_control = cmds.curve(name=f"{self.side}pelvis_{self.module_nr}_CTRL", pointWeight=cube_points, degree=1)
        cmds.addAttr(pelvis_control, niceName="module", longName="module", attributeType="message", readable=True,
                     writable=True)
        cmds.setAttr(f"{pelvis_control}.rotateOrder", RotateOrder.YZX)
        cmds.matchTransform(pelvis_control, pelvis_mch, position=True, rotation=False, scale=False)
        bake_transform_to_offset_parent_matrix(pelvis_control)
        cmds.parent(pelvis_mch, pelvis_control)

        back_control = cmds.curve(name=f"{self.side}back_{self.module_nr}_CTRL", pointWeight=cube_points, degree=1)
        cmds.addAttr(back_control, niceName="module", longName="module", attributeType="message", readable=True,
                     writable=True)
        cmds.setAttr(f"{back_control}.rotateOrder", RotateOrder.YZX)
        cmds.matchTransform(back_control, back_mch, position=True, rotation=False, scale=False)
        bake_transform_to_offset_parent_matrix(back_control)
        cmds.parent(back_mch, back_control)

        chest_control = cmds.curve(name=f"{self.side}chest_{self.module_nr}_CTRL", pointWeight=cube_points, degree=1)
        cmds.addAttr(chest_control, niceName="module", longName="module", attributeType="message", readable=True,
                     writable=True)
        cmds.setAttr(f"{chest_control}.rotateOrder", RotateOrder.YZX)
        cmds.matchTransform(chest_control, chest_mch, position=True, rotation=False, scale=False)
        bake_transform_to_offset_parent_matrix(chest_control)
        cmds.parent(chest_mch, chest_control)

        curve_points = [
            cmds.xform(f"{segment}_JNT", query=True, translation=True, worldSpace=True) for segment in segments
        ]

        spline_curve = cmds.curve(name=f"{self.side}spine_{self.module_nr}_curve", point=curve_points, degree=4)

        spline_handle = cmds.ikHandle(
            name=f"{self.side}spine_{self.module_nr}_ikHandle", startJoint=f"{segments[0]}_IK",
            endEffector=f"{segments[-1]}_IK",
            solver="ikSplineSolver", createCurve=False, parentCurve=False, curve=spline_curve
        )[0]

        cmds.skinCluster(pelvis_mch, back_mch, chest_mch, spline_curve, maximumInfluences=5, bindMethod=0, skinMethod=0)

        cmds.setAttr(f"{spline_handle}.dTwistControlEnable", True)
        cmds.setAttr(f"{spline_handle}.dWorldUpType", WorldUpType.OBJECT_ROTATION_UP_START_END.value)
        cmds.setAttr(f"{spline_handle}.dForwardAxis", ForwardAxis.POSITIVE_Y.value)
        cmds.setAttr(f"{spline_handle}.dWorldUpAxis", UpAxis.POSITIVE_Z.value)
        cmds.setAttr(f"{spline_handle}.dWorldUpVectorX", 0)
        cmds.setAttr(f"{spline_handle}.dWorldUpVectorY", 0)
        cmds.setAttr(f"{spline_handle}.dWorldUpVectorZ", 1)
        cmds.setAttr(f"{spline_handle}.dWorldUpVectorEndX", 0)
        cmds.setAttr(f"{spline_handle}.dWorldUpVectorEndY", 0)
        cmds.setAttr(f"{spline_handle}.dWorldUpVectorEndZ", 1)
        cmds.connectAttr(f"{pelvis_mch}.worldMatrix", f"{spline_handle}.dWorldUpMatrix")
        cmds.connectAttr(f"{chest_mch}.worldMatrix", f"{spline_handle}.dWorldUpMatrixEnd")

        return [pelvis_control, back_control, chest_control, pelvis_mch, back_mch, chest_mch], spline_curve

    def spring_kinematic(self, segments):
        knee_handle = cmds.ikHandle(name=f"{self.prefix}_knee_ikRPsolver",
                                    startJoint=f"{segments[0]}_IK",
                                    endEffector=f"{segments[2]}_IK",
                                    solver="ikRPsolver")[0]

        hoc_handle = cmds.ikHandle(name=f"{self.prefix}_hoc_ikSCsolver_#",
                                   startJoint=f"{segments[2]}_IK",
                                   endEffector=f"{segments[3]}_IK",
                                   solver="ikSCsolver")[0]

        toe_handle = cmds.ikHandle(name=f"{self.prefix}_toe_ikSCsolver_#",
                                   startJoint=f"{segments[3]}_IK",
                                   endEffector=f"{segments[4]}_IK",
                                   solver="ikSCsolver")[0]

        ik_control = cmds.curve(name=f"{self.prefix}_IK_CTRL", pointWeight=cube_points, degree=1)
        cmds.matchTransform(ik_control, f"{segments[3]}_IK", rotation=True, position=True, scale=False)
        cmds.setAttr(f"{ik_control}.rotateOrder", RotateOrder.YZX)

        hoc_control = cmds.curve(name=f"{self.prefix}_HOC_CTRL", pointWeight=cube_points, degree=1)
        cmds.setAttr(f"{hoc_control}.rotateOrder", RotateOrder.YZX)
        cmds.matchTransform(hoc_control, f"{segments[2]}_IK")
        position = cmds.xform(f"{segments[3]}_IK", query=True, translation=True, worldSpace=True)
        cmds.parent(hoc_control, ik_control)

        pole_control = cmds.curve(name=f"{self.prefix}_POLE_CTRL", pointWeight=cube_points, degree=1)
        cmds.setAttr(f"{pole_control}.rotateOrder", RotateOrder.YZX)
        cmds.matchTransform(pole_control, f"{segments[1]}_IK", position=True, rotation=False, scale=False)
        # cmds.move(0, 0, 20, pole_control, relative=True, objectSpace=True)
        cmds.poleVectorConstraint(pole_control, knee_handle)

        cmds.parent(knee_handle, hoc_control)
        cmds.parent(hoc_handle, ik_control)
        cmds.parent(toe_handle, ik_control)

        bake_transform_to_offset_parent_matrix(ik_control)
        bake_transform_to_offset_parent_matrix(hoc_control)
        bake_transform_to_offset_parent_matrix(pole_control)

        cmds.move(*position, f"{hoc_control}.scalePivot", f"{hoc_control}.rotatePivot", absolute=True)

        return [ik_control, pole_control, hoc_control]

    def switch_kinematic(self, fk_joints, fk_controls, ik_joints, ik_controls):
        switch_control = "switch_control"
        if not cmds.objExists(switch_control):
            cmds.curve(name=switch_control, pointWeight=cube_points, degree=1)

        attribute = f"{self.prefix}_switch"
        if not cmds.attributeQuery(attribute, node=switch_control, exists=True):
            cmds.addAttr(
                switch_control, attributeType="float", niceName=attribute,
                longName=attribute, defaultValue=0, minValue=0, maxValue=1, keyable=True
            )

        switch_control_reversed = cmds.createNode("reverse", name=f"{self.prefix}_switch_reversed")
        cmds.connectAttr(f"{switch_control}.{attribute}", f"{switch_control_reversed}.inputX")

        for ik_joint in ik_joints:
            cmds.connectAttr(f"{switch_control}.{attribute}",
                             f"{ik_joint.replace('IK', 'JNT')}_parentConstraint1.{ik_joint}W1")
            cmds.connectAttr(f"{switch_control}.{attribute}", f"{ik_joint}.visibility")

        for fk_joint in fk_joints:
            cmds.connectAttr(f"{switch_control_reversed}.outputX",
                             f"{fk_joint.replace('FK', 'JNT')}_parentConstraint1.{fk_joint}W0")
            cmds.connectAttr(f"{switch_control_reversed}.outputX", f"{fk_joint}.visibility")

        for ik_control in ik_controls:
            cmds.connectAttr(f"{switch_control}.{attribute}", f"{ik_control}.visibility")
            cmds.addAttr(ik_control, longName=attribute, proxy=f"{switch_control}.{attribute}")

        for fk_control in fk_controls:
            cmds.connectAttr(f"{switch_control_reversed}.outputX", f"{fk_control}.visibility")
            cmds.addAttr(fk_control, longName=attribute, proxy=f"{switch_control}.{attribute}")

    def inverse_kinematic_space_swap(self, ik_control, pole_control):
        cmds.addAttr(pole_control, attributeType="enum", enumName=f"world=0:{self.name}=1", niceName="follow",
                     longName="follow", defaultValue=0, keyable=True)

        cmds.addAttr(ik_control, longName=f"follow", proxy=f"{pole_control}.follow")

        space_swap = cmds.createNode("blendMatrix", name=f"{self.name}_blend_matrix_space_swap_#")
        offset_matrix = cmds.getAttr(f"{pole_control}.offsetParentMatrix")
        cmds.setAttr(f"{space_swap}.inputMatrix", offset_matrix, type="matrix")

        ik_swap_position = cmds.spaceLocator(name=f"{self.name}_ik_swap_position_#")[0]
        cmds.setAttr(f"{ik_swap_position}.visibility", False)
        cmds.matchTransform(ik_swap_position, pole_control, position=True, rotation=True, scale=False)
        cmds.parent(ik_swap_position, ik_control)

        bake_transform_to_offset_parent_matrix(ik_swap_position)

        cmds.connectAttr(f"{ik_swap_position}.worldMatrix[0]", f"{space_swap}.target[0].targetMatrix")
        cmds.connectAttr(f"{space_swap}.outputMatrix", f"{pole_control}.offsetParentMatrix")
        cmds.connectAttr(f"{pole_control}.follow", f"{space_swap}.envelope")
