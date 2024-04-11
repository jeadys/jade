import maya.cmds as cmds

from joints.joint_layer import create_layer_joints

from utilities.curve import Curve
from utilities.enums import WorldUpType, ForwardAxis, UpAxis
from utilities.bake_transform import bake_transform_to_offset_parent_matrix


class SplineChain:
    def __init__(self, prefix, name) -> None:
        self.prefix = prefix
        self.name = name
        self.kinematic_parent_group = f"{self.prefix}_{self.name}_kinematics"
        self.control_parent_group = f"{self.prefix}_{self.name}_controls"
        self.control_shape: Curve = Curve()
        self.curve_points: list[list[float, float, float]] = []

    def create_spline_joints(self, segments: list[str]) -> list[str]:
        spline_joints = create_layer_joints(name=self.name, prefix=self.prefix, layer_name="IK", segments=segments)
        return spline_joints

    def create_spline_curve(self, segments: list[str]) -> None:
        for index, joint in enumerate(segments):
            # We want to create a custom curve instead of an auto generated one for the IK SPLINE
            joint_position: list[float, float, float] = cmds.xform(joint, query=True, translation=True, worldSpace=True)
            self.curve_points.append(joint_position)

        cmds.select(deselect=True)
        pelvis_mch: str = cmds.joint(radius=3, rotationOrder="zxy", name=f"pelvis_MCH")
        cmds.matchTransform(pelvis_mch, f"{segments[0]}", position=True, rotation=False, scale=False)

        back_mch: str = cmds.joint(radius=3, rotationOrder="zxy", name=f"back_MCH")
        cmds.matchTransform(back_mch, f"{segments[len(segments) // 2]}", position=True, rotation=False,
                            scale=False)
        # We need to get the center between the start/end of the segments when the number pf segments is an even number.
        if len(segments) % 2 == 0:
            constraint = cmds.parentConstraint([segments[0], segments[-1]], back_mch,
                                               maintainOffset=False, skipTranslate=["x", "z"],
                                               skipRotate=["x", "y", "z"])
            cmds.delete(constraint)
        cmds.parent(back_mch, world=True)

        chest_mch: str = cmds.joint(radius=3, rotationOrder="zxy", name=f"chest_MCH")
        cmds.matchTransform(chest_mch, f"{segments[-1]}", position=True, rotation=False, scale=False)
        cmds.parent(chest_mch, world=True)

        for joint in [pelvis_mch, back_mch, chest_mch]:
            cmds.setAttr(f"{joint}.radius", 5)
            bake_transform_to_offset_parent_matrix(joint)

        spline_curve: str = cmds.curve(
            name=f"{self.name}_curve_spline",
            point=self.curve_points,
            degree=4,
        )

        spline_handle: str = cmds.ikHandle(
            name=f"{self.name}_ikHandle_spline",
            startJoint=f"{segments[0]}",
            endEffector=f"{segments[-1]}",
            solver="ikSplineSolver",
            createCurve=False,
            parentCurve=False,
            curve=spline_curve
        )[0]

        cmds.skinCluster(
            pelvis_mch, back_mch, chest_mch, spline_curve,
            maximumInfluences=5, bindMethod=0, skinMethod=0
        )

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

    def create_spline_controls(self) -> list[str]:
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        cog_ctrl: str = self.control_shape.curve_four_way_arrow(name="cog_CTRL", scale=5)
        pelvis_ctrl: str = self.control_shape.curve_circle(name="pelvis_CTRL", scale=5)
        back_ctrl: str = self.control_shape.curve_two_way_arrow(name="back_CTRL")
        chest_ctrl: str = self.control_shape.curve_chest(name="chest_CTRL")

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

        cmds.parent("pelvis_MCH", pelvis_ctrl)
        cmds.parent("back_MCH", back_ctrl)
        cmds.parent("chest_MCH", chest_ctrl)

        return [cog_ctrl, pelvis_ctrl, back_ctrl, chest_ctrl]
        # IK NODES
        # cmds.connectAttr(f"{pelvis_ctrl}.worldMatrix[0]", f"pelvis_MCH.offsetParentMatrix")
        # cmds.connectAttr(f"{back_ctrl}.worldMatrix[0]", f"back_MCH.offsetParentMatrix")
        # cmds.connectAttr(f"{chest_ctrl}.worldMatrix[0]", f"chest_MCH.offsetParentMatrix")

        # cmds.connectAttr(f"{pelvis_ctrl}.translate", f"pelvis_MCH.translate")
        # cmds.connectAttr(f"{pelvis_ctrl}.rotate", f"pelvis_MCH.rotate")
        #
        # cmds.connectAttr(f"{back_ctrl}.translate", f"back_MCH.translate")
        # cmds.connectAttr(f"{back_ctrl}.rotate", f"back_MCH.rotate")
        #
        # cmds.connectAttr(f"{chest_ctrl}.translate", f"chest_MCH.translate")
        # cmds.connectAttr(f"{chest_ctrl}.rotate", f"chest_MCH.rotate")
