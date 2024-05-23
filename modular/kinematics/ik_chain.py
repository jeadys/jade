import maya.cmds as cmds

from modular.biped.biped import Segment

from utilities.curve import select_curve
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.enums import Shape, WorldUpType, ForwardAxis, UpAxis


class IKChain:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def ik_joint(self, prefix, segments: list[Segment]) -> list[str]:
        joint_group = cmds.group(empty=True, name=f"{prefix}{self.name}_{self.blueprint_nr}_IK_GROUP")

        joint_layer_group = f"{prefix}{self.name}_{self.blueprint_nr}_LAYER_GROUP"
        if not cmds.objExists(joint_layer_group):
            joint_layer_group = cmds.group(empty=True, name=joint_layer_group)
        cmds.parent(joint_group, joint_layer_group)

        ik_joints = []
        for segment in segments:
            if cmds.objExists(f"{prefix}{segment.name}_{self.blueprint_nr}_IK"):
                continue

            current_segment = cmds.duplicate(f"{prefix}{segment.name}_{self.blueprint_nr}_JNT",
                                             name=f"{prefix}{segment.name}_{self.blueprint_nr}_IK", parentOnly=True)[0]
            cmds.parentConstraint(current_segment, f"{prefix}{segment.name}_{self.blueprint_nr}_JNT",
                                  maintainOffset=True)

            if segment.control.parent is not None:
                cmds.parent(current_segment, f"{prefix}{segment.parent.name}_{self.blueprint_nr}_IK")
            else:
                cmds.parent(current_segment, joint_group)

            ik_joints.append(current_segment)

        if self.selection and cmds.objExists(f"{prefix}{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{prefix}{self.selection[0]}_JNT", joint_group, maintainOffset=True)
        elif self.selection and not cmds.objExists(f"{prefix}{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{self.selection[0]}_JNT", joint_group, maintainOffset=True)

        return ik_joints

    def ik_control(self, prefix, segments: list[Segment]) -> list[str]:
        control_group = cmds.group(empty=True, name=f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL_GROUP")

        joint_control_group = f"{prefix}{self.name}_{self.blueprint_nr}_CONTROL_GROUP"
        if not cmds.objExists(joint_control_group):
            cmds.group(empty=True, name=joint_control_group)
        cmds.parent(control_group, joint_control_group)

        ik_control = select_curve(shape=Shape.CUBE, name=f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL", scale=5)
        pole_control = select_curve(shape=Shape.CUBE, name=f"{prefix}{self.name}_{self.blueprint_nr}_POLE_CTRL",
                                    scale=5)

        ik_handle = cmds.ikHandle(name=f"{prefix}{self.name}_{self.blueprint_nr}_ikHandle",
                                  startJoint=f"{prefix}{segments[0].name}_{self.blueprint_nr}_IK",
                                  endEffector=f"{prefix}{segments[-1].name}_{self.blueprint_nr}_IK",
                                  solver="ikRPsolver")[0]

        cmds.matchTransform(ik_control, f"{prefix}{segments[-1].name}_{self.blueprint_nr}_IK", position=True,
                            rotation=True, scale=False)
        cmds.parent(ik_handle, ik_control)
        cmds.orientConstraint(ik_control, f"{prefix}{segments[-1].name}_{self.blueprint_nr}_IK", maintainOffset=True)

        cmds.matchTransform(pole_control, f"{prefix}{segments[1].name}_{self.blueprint_nr}_IK", position=True,
                            rotation=True, scale=False)
        # cmds.move(0, 0, -50, pole_control, relative=True, worldSpace=True)
        cmds.poleVectorConstraint(pole_control, ik_handle)

        cmds.parent(ik_control, control_group)
        cmds.parent(pole_control, control_group)

        bake_transform_to_offset_parent_matrix(ik_control)
        bake_transform_to_offset_parent_matrix(pole_control)

        # if self.selection and cmds.objExists(f"{prefix}{self.selection[0]}_JNT"):
        #     cmds.parentConstraint(f"{prefix}{self.selection[0]}_JNT", control_group, maintainOffset=True)
        # elif self.selection and not cmds.objExists(f"{prefix}{self.selection[0]}_JNT"):
        #     cmds.parentConstraint(f"{self.selection[0]}_JNT", control_group, maintainOffset=True)

        return [ik_control, pole_control]

    def spline_kinematic(self, segments):
        pelvis_mch = cmds.joint(radius=3, rotationOrder="zxy", name=f"pelvis_{self.blueprint_nr}_MCH")
        cmds.matchTransform(pelvis_mch, f"{segments[0].name}_{self.blueprint_nr}_JNT", position=True, rotation=False,
                            scale=False)

        back_mch = cmds.joint(radius=3, rotationOrder="zxy", name=f"back_{self.blueprint_nr}_MCH")
        cmds.matchTransform(back_mch, f"{segments[len(segments) // 2].name}_{self.blueprint_nr}_JNT", position=True,
                            rotation=False,
                            scale=False)
        # We need to get the center between the start/end of the segments when the number pf segments is an even number.
        if len(segments) % 2 == 0:
            constraint = cmds.parentConstraint(
                [f"{segments[0].name}_{self.blueprint_nr}_JNT", f"{segments[-1].name}_{self.blueprint_nr}_JNT"],
                back_mch,
                maintainOffset=False, skipTranslate=["x", "z"], skipRotate=["x", "y", "z"])
            cmds.delete(constraint)
        cmds.parent(back_mch, world=True)

        chest_mch = cmds.joint(radius=3, rotationOrder="zxy", name=f"chest_{self.blueprint_nr}_MCH")
        cmds.matchTransform(chest_mch, f"{segments[-1].name}_{self.blueprint_nr}_JNT", position=True, rotation=False,
                            scale=False)
        cmds.parent(chest_mch, world=True)

        cmds.setAttr(f"{pelvis_mch}.radius", 5)
        bake_transform_to_offset_parent_matrix(pelvis_mch)

        cmds.setAttr(f"{back_mch}.radius", 5)
        bake_transform_to_offset_parent_matrix(back_mch)

        cmds.setAttr(f"{chest_mch}.radius", 5)
        bake_transform_to_offset_parent_matrix(chest_mch)

        pelvis_control = select_curve(shape=Shape.CUBE, name=f"pelvis_{self.blueprint_nr}_CTRL", scale=5)
        cmds.addAttr(pelvis_control, niceName="blueprint", longName="blueprint", attributeType="message", readable=True,
                     writable=True)
        cmds.matchTransform(pelvis_control, pelvis_mch, position=True, rotation=False, scale=False)
        bake_transform_to_offset_parent_matrix(pelvis_control)
        cmds.parent(pelvis_mch, pelvis_control)

        back_control = select_curve(shape=Shape.CUBE, name=f"back_{self.blueprint_nr}_CTRL", scale=5)
        cmds.addAttr(back_control, niceName="blueprint", longName="blueprint", attributeType="message", readable=True,
                     writable=True)
        cmds.matchTransform(back_control, back_mch, position=True, rotation=False, scale=False)
        bake_transform_to_offset_parent_matrix(back_control)
        cmds.parent(back_mch, back_control)

        chest_control = select_curve(shape=Shape.CUBE, name=f"chest_{self.blueprint_nr}_CTRL", scale=5)
        cmds.addAttr(chest_control, niceName="blueprint", longName="blueprint", attributeType="message", readable=True,
                     writable=True)
        cmds.matchTransform(chest_control, chest_mch, position=True, rotation=False, scale=False)
        bake_transform_to_offset_parent_matrix(chest_control)
        cmds.parent(chest_mch, chest_control)

        curve_points = [
            cmds.xform(f"{segment.name}_{self.blueprint_nr}_JNT", query=True, translation=True, worldSpace=True)
            for segment in segments]
        spline_curve = cmds.curve(name=f"spine_{self.blueprint_nr}_curve", point=curve_points, degree=4)

        spline_handle = cmds.ikHandle(
            name=f"spine_{self.blueprint_nr}_ikHandle", startJoint=f"{segments[0].name}_{self.blueprint_nr}_IK",
            endEffector=f"{segments[-1].name}_{self.blueprint_nr}_IK",
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

        return [pelvis_control, back_control, chest_control, pelvis_mch, back_mch, chest_mch]

    def spring_kinematic(self, prefix, segments):
        for segment in segments:
            if cmds.objExists(f"{prefix}{segment.name}_{self.blueprint_nr}_IK"):
                continue

            current_segment = cmds.duplicate(f"{prefix}{segment.name}_{self.blueprint_nr}_JNT",
                                             name=f"{prefix}{segment.name}_{self.blueprint_nr}_IK", parentOnly=True)[0]
            cmds.parentConstraint(current_segment, f"{prefix}{segment.name}_{self.blueprint_nr}_JNT",
                                  maintainOffset=True)

            if segment.parent is not None:
                cmds.parent(current_segment, f"{prefix}{segment.parent}_{self.blueprint_nr}_IK")

        knee_handle = cmds.ikHandle(name=f"{prefix}{self.name}_{self.blueprint_nr}_knee_ikRPsolver",
                                    startJoint=f"{prefix}{segments[0].name}_{self.blueprint_nr}_IK",
                                    endEffector=f"{prefix}{segments[2].name}_{self.blueprint_nr}_IK",
                                    solver="ikRPsolver")[0]

        hoc_handle = cmds.ikHandle(name=f"{prefix}{self.name}_{self.blueprint_nr}_hoc_ikSCsolver_#",
                                   startJoint=f"{prefix}{segments[2].name}_{self.blueprint_nr}_IK",
                                   endEffector=f"{prefix}{segments[3].name}_{self.blueprint_nr}_IK",
                                   solver="ikSCsolver")[0]

        toe_handle = cmds.ikHandle(name=f"{prefix}{self.name}_{self.blueprint_nr}_toe_ikSCsolver_#",
                                   startJoint=f"{prefix}{segments[3].name}_{self.blueprint_nr}_IK",
                                   endEffector=f"{prefix}{segments[4].name}_{self.blueprint_nr}_IK",
                                   solver="ikSCsolver")[0]

        ik_control = select_curve(shape=Shape.CUBE, name=f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL", scale=5)
        cmds.matchTransform(ik_control, f"{prefix}{segments[3].name}_{self.blueprint_nr}_IK", rotation=True,
                            position=True, scale=False)

        hoc_control = select_curve(shape=Shape.CUBE, name=f"{prefix}{self.name}_{self.blueprint_nr}_HOC_CTRL", scale=5)
        cmds.matchTransform(hoc_control, f"{prefix}{segments[2].name}_{self.blueprint_nr}_IK")
        position = cmds.xform(f"{prefix}{segments[3].name}_{self.blueprint_nr}_IK", query=True, translation=True,
                              worldSpace=True)
        cmds.parent(hoc_control, ik_control)

        pole_control = select_curve(shape=Shape.CUBE, name=f"{prefix}{self.name}_{self.blueprint_nr}_POLE_CTRL",
                                    scale=5)
        cmds.matchTransform(pole_control, f"{prefix}{segments[1].name}_{self.blueprint_nr}_IK", position=True,
                            rotation=False, scale=False)
        cmds.move(0, 0, 20 if prefix == "L" else 20, pole_control, relative=True, objectSpace=True)
        cmds.poleVectorConstraint(pole_control, knee_handle)
        # cmds.parent(pole_control, ik_control)

        cmds.parent(knee_handle, hoc_control)
        cmds.parent(hoc_handle, ik_control)
        cmds.parent(toe_handle, ik_control)

        bake_transform_to_offset_parent_matrix(ik_control)
        bake_transform_to_offset_parent_matrix(hoc_control)
        bake_transform_to_offset_parent_matrix(pole_control)

        cmds.move(*position, f"{hoc_control}.scalePivot", f"{hoc_control}.rotatePivot", absolute=True)

        return [ik_control, pole_control, hoc_control]

    def switch_kinematic(self, prefix, fk_joints, fk_controls, ik_joints, ik_controls):
        switch_control = "switch_control"
        if not cmds.objExists(switch_control):
            select_curve(shape=Shape.CUBE, name=switch_control, scale=2.5)

        attribute = f"{prefix}{self.name}_{self.blueprint_nr}_switch"
        if not cmds.attributeQuery(attribute, node=switch_control, exists=True):
            cmds.addAttr(
                switch_control, attributeType="float", niceName=attribute,
                longName=attribute, defaultValue=0, minValue=0, maxValue=1, keyable=True
            )

        switch_control_reversed = cmds.createNode("reverse",
                                                  name=f"{prefix}{self.name}_{self.blueprint_nr}_switch_reversed")
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
                     longName="follow",
                     defaultValue=0, keyable=True)

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
