import maya.cmds as cmds
import mechanisms.spine_stretch as spine_stretch_module
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.curve import Curve
from importlib import reload
import utilities.curve as control_shape
from utilities.enums import WorldUpType, ForwardAxis, UpAxis

reload(control_shape)
reload(spine_stretch_module)


# @dataclass(frozen=True)
# class SpineSegment:
#     name: str
#     shape: str


class IKSpine:
    def __init__(self, prefix, spine_count) -> None:
        self.prefix = prefix
        self.spine_count = spine_count
        self.spine_segments = [f"{self.prefix}_spine_0{spine + 1}" for spine in range(self.spine_count)]

        self.kinematic_parent_group = f"{self.prefix}_spine_kinematics"
        self.control_parent_group = f"{self.prefix}_spine_controls"
        self.control_shape: Curve = Curve()
        self.curve_points = []

    def create_ik_spine(self):
        # self.create_ik_spine_joints()
        self.create_ik_spine_curve()
        self.create_ik_spine_controls()

    def create_ik_spine_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_ik_joint = self.kinematic_parent_group
        for index, joint in enumerate(self.spine_segments):
            current_ik_joint = cmds.duplicate(joint, parentOnly=True, name=f"{joint}_IK")[0]
            cmds.parentConstraint(current_ik_joint, joint, maintainOffset=True)
            cmds.parent(current_ik_joint, previous_ik_joint)

            bake_transform_to_offset_parent_matrix(current_ik_joint)

            previous_ik_joint = current_ik_joint

            # We want to create a custom curve instead of an auto generated one for the IK SPLINE
            joint_position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
            joint_points = (joint_position[0], joint_position[1], joint_position[2])
            self.curve_points.append(joint_points)

    def create_ik_spine_curve(self):

        for index, joint in enumerate(self.spine_segments):
            # We want to create a custom curve instead of an auto generated one for the IK SPLINE
            joint_position = cmds.xform(joint, query=True, translation=True, worldSpace=True)
            joint_points = (joint_position[0], joint_position[1], joint_position[2])
            self.curve_points.append(joint_points)

        cmds.select(deselect=True)
        pelvis_mch = cmds.joint(radius=3, rotationOrder="zxy", name=f"pelvis_MCH")
        cmds.matchTransform(pelvis_mch, f"{self.spine_segments[0]}", position=True, rotation=False, scale=False)

        back_mch = cmds.joint(radius=3, rotationOrder="zxy", name=f"back_MCH")
        cmds.matchTransform(back_mch, f"{self.spine_segments[len(self.spine_segments) // 2]}", position=True, rotation=False, scale=False)
        # We need to get the center between the start and end of the spine when the number is spines is an even number.
        if len(self.spine_segments) % 2 == 0:
            constraint = cmds.parentConstraint([self.spine_segments[0], self.spine_segments[-1]], back_mch,
                                               maintainOffset=False, skipTranslate=["x", "z"],
                                               skipRotate=["x", "y", "z"])
            cmds.delete(constraint)
        cmds.parent(back_mch, world=True)

        chest_mch = cmds.joint(radius=3, rotationOrder="zxy", name=f"chest_MCH")
        cmds.matchTransform(chest_mch, f"{self.spine_segments[-1]}", position=True, rotation=False, scale=False)
        cmds.parent(chest_mch, world=True)

        for joint in [pelvis_mch, back_mch, chest_mch]:
            cmds.setAttr(f"{joint}.radius", 5)
            bake_transform_to_offset_parent_matrix(joint)

        curve_spine = cmds.curve(
            name="curve_spine",
            point=self.curve_points,
            degree=4,
        )

        spine_handle = cmds.ikHandle(
            name="ikHandle_spine",
            startJoint=f"{self.spine_segments[0]}",
            endEffector=f"{self.spine_segments[-1]}",
            solver="ikSplineSolver",
            createCurve=False,
            parentCurve=False,
            curve=curve_spine
        )[0]

        cmds.skinCluster(
            pelvis_mch, back_mch, chest_mch, curve_spine,
            maximumInfluences=5, bindMethod=0, skinMethod=0
        )

        cmds.setAttr(f"{spine_handle}.dTwistControlEnable", True)
        cmds.setAttr(f"{spine_handle}.dWorldUpType", WorldUpType.OBJECT_ROTATION_UP_START_END.value)
        cmds.setAttr(f"{spine_handle}.dForwardAxis", ForwardAxis.POSITIVE_Y.value)
        cmds.setAttr(f"{spine_handle}.dWorldUpAxis", UpAxis.POSITIVE_Z.value)
        cmds.setAttr(f"{spine_handle}.dWorldUpVectorX", 0)
        cmds.setAttr(f"{spine_handle}.dWorldUpVectorY", 0)
        cmds.setAttr(f"{spine_handle}.dWorldUpVectorZ", 1)
        cmds.setAttr(f"{spine_handle}.dWorldUpVectorEndX", 0)
        cmds.setAttr(f"{spine_handle}.dWorldUpVectorEndY", 0)
        cmds.setAttr(f"{spine_handle}.dWorldUpVectorEndZ", 1)
        cmds.connectAttr(f"{pelvis_mch}.worldMatrix", f"{spine_handle}.dWorldUpMatrix")
        cmds.connectAttr(f"{chest_mch}.worldMatrix", f"{spine_handle}.dWorldUpMatrixEnd")

    def create_ik_spine_controls(self):
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        cog_ctrl = self.control_shape.curve_four_way_arrow(name="cog_CTRL")
        pelvis_ctrl = self.control_shape.curve_circle(name="pelvis_CTRL")
        back_ctrl = self.control_shape.curve_two_way_arrow(name="back_CTRL")
        chest_ctrl = self.control_shape.curve_chest(name="chest_CTRL")

        cmds.parent(pelvis_ctrl, cog_ctrl)
        cmds.parent(back_ctrl, cog_ctrl)
        cmds.parent(chest_ctrl, cog_ctrl)

        cmds.matchTransform(cog_ctrl, f"pelvis_MCH", position=True, rotation=False, scale=False)
        cmds.matchTransform(pelvis_ctrl, f"pelvis_MCH", position=True, rotation=False, scale=False)
        cmds.matchTransform(back_ctrl, f"back_MCH", position=True, rotation=False, scale=False)
        cmds.matchTransform(chest_ctrl, f"chest_MCH", position=True, rotation=False, scale=False)

        bake_transform_to_offset_parent_matrix(cog_ctrl)
        bake_transform_to_offset_parent_matrix(pelvis_ctrl)
        bake_transform_to_offset_parent_matrix(back_ctrl)
        bake_transform_to_offset_parent_matrix(chest_ctrl)

        # IK NODES
        cmds.connectAttr(f"{pelvis_ctrl}.worldMatrix[0]", f"pelvis_MCH.offsetParentMatrix")
        # cmds.connectAttr(f"{back_ctrl}.worldMatrix[0]", f"back_MCH.offsetParentMatrix")
        # cmds.connectAttr(f"{chest_ctrl}.worldMatrix[0]", f"chest_MCH.offsetParentMatrix")

        # cmds.connectAttr(f"{pelvis_ctrl}.translate", f"pelvis_MCH.translate")
        # cmds.connectAttr(f"{pelvis_ctrl}.rotate", f"pelvis_MCH.rotate")

        cmds.connectAttr(f"{back_ctrl}.translate", f"back_MCH.translate")
        cmds.connectAttr(f"{back_ctrl}.rotate", f"back_MCH.rotate")

        cmds.connectAttr(f"{chest_ctrl}.translate", f"chest_MCH.translate")
        cmds.connectAttr(f"{chest_ctrl}.rotate", f"chest_MCH.rotate")



