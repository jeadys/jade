from importlib import reload

import maya.cmds as cmds

import utilities.curve as control_shape
from utilities.curve import Curve

reload(control_shape)


class SwitchSpine:
    def __init__(self) -> None:
        self.control_shape: Curve = Curve()

    def create_ik_fk_switch_spine_control(self, control_name: str, connected_limb: str):
        ik_fk_switch_offset = cmds.group(empty=True, name=f"SWITCH_OFFSET_{control_name}")

        ik_fk_switch_ctrl = self.control_shape.curve_two_way_arrow(name=f"SWITCH_CTRL_{control_name}")

        cmds.setAttr(f"{ik_fk_switch_ctrl}.overrideEnabled", 1)
        cmds.setAttr(f"{ik_fk_switch_ctrl}.overrideColor", 12)

        cmds.parent(ik_fk_switch_ctrl, ik_fk_switch_offset)

        cmds.matchTransform(ik_fk_switch_offset, f"DEF_{connected_limb}", position=True, rotation=False, scale=False)
        position = cmds.xform(ik_fk_switch_offset, query=True, translation=True, worldSpace=True)
        cmds.move(position[0] * 1.75, position[1], position[2] - 25, ik_fk_switch_offset)
        cmds.addAttr(
            ik_fk_switch_ctrl, attributeType="float", niceName="IK_FK_SWITCH", longName="IK_FK_SWITCH", defaultValue=0,
            minValue=0, maxValue=1, keyable=True
        )

        ik_text_curve = self.control_shape.curve_text(name=f"IK_TEXT_{control_name}_curve", text="IK")
        cmds.matchTransform(ik_text_curve, f"SWITCH_CTRL_{control_name}", position=True, rotation=False, scale=False)
        cmds.parent(ik_text_curve, ik_fk_switch_offset)

        fk_text_curve = self.control_shape.curve_text(name=f"FK_TEXT_{control_name}_curve", text="FK")
        cmds.matchTransform(fk_text_curve, f"SWITCH_CTRL_{control_name}", position=True, rotation=False, scale=False)
        cmds.parent(fk_text_curve, ik_fk_switch_offset)

        self.create_ik_fk_switch_spine_constraints(control_name=control_name, ik_fk_switch_ctrl=ik_fk_switch_ctrl)
        self.create_ik_fk_switch_spine_attribute_proxies(ik_fk_switch_ctrl=ik_fk_switch_ctrl)

        return ik_fk_switch_offset, ik_fk_switch_ctrl

    @staticmethod
    def create_ik_fk_switch_spine_constraints(control_name: str, ik_fk_switch_ctrl):
        reverse_node = cmds.createNode("reverse", name=f"IK_FK_SWITCH_{control_name}_REVERSED")

        # spine IK SWITCH
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"DEF_pelvis_parentConstraint1.IK_pelvisW1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"DEF_spine_01_parentConstraint1.IK_spine_01W1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"DEF_spine_02_parentConstraint1.IK_spine_02W1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"DEF_spine_03_parentConstraint1.IK_spine_03W1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"DEF_neck_parentConstraint1.IK_neckW1")

        # hide/unhide IK spine controls
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"IK_OFFSET_cog.visibility")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"IK_TEXT_{control_name}_curveShape.visibility")

        # Only when the arms are created before the spine
        if cmds.objExists("L_FK_OFFSET_humerus") and cmds.objExists("L_arm_group_IK"):
            cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"L_arm_group_parentConstraint1.L_arm_group_IKW1")
            cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                             f"L_FK_OFFSET_humerus_parentConstraint1.L_arm_group_IKW1")

        # Reverse IK >< FK switch
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{reverse_node}.inputX")

        # spine FK SWITCH
        cmds.connectAttr(f"{reverse_node}.outputX", f"DEF_pelvis_parentConstraint1.FK_pelvisW0")
        cmds.connectAttr(f"{reverse_node}.outputX", f"DEF_spine_01_parentConstraint1.FK_spine_01W0")
        cmds.connectAttr(f"{reverse_node}.outputX", f"DEF_spine_02_parentConstraint1.FK_spine_02W0")
        cmds.connectAttr(f"{reverse_node}.outputX", f"DEF_spine_03_parentConstraint1.FK_spine_03W0")
        cmds.connectAttr(f"{reverse_node}.outputX", f"DEF_neck_parentConstraint1.FK_neckW0")

        # hide/unhide FK spine controls
        cmds.connectAttr(f"{reverse_node}.outputX", f"FK_OFFSET_pelvis.visibility")
        cmds.connectAttr(f"{reverse_node}.outputX", f"FK_TEXT_{control_name}_curveShape.visibility")

        # Only when the arms are created before the spine
        if cmds.objExists("L_FK_OFFSET_humerus") and cmds.objExists("L_arm_group_FK"):
            cmds.connectAttr(f"{reverse_node}.outputX", f"L_arm_group_parentConstraint1.L_arm_group_FKW0")
            cmds.connectAttr(f"{reverse_node}.outputX", f"L_FK_OFFSET_humerus_parentConstraint1.L_arm_group_FKW0")

    @staticmethod
    def create_ik_fk_switch_spine_attribute_proxies(ik_fk_switch_ctrl):
        # CONTROL IK FK SWITCH THROUGH FK CONTROLS ATTRIBUTE
        cmds.addAttr("FK_CTRL_pelvis", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr("FK_CTRL_spine_01", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr("FK_CTRL_spine_02", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr("FK_CTRL_spine_03", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")

        # CONTROL IK FK SWITCH THROUGH IK CONTROLS ATTRIBUTE
        cmds.addAttr("IK_CTRL_cog", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr("IK_CTRL_hip", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr("IK_CTRL_pelvis", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr("IK_CTRL_chest", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr("IK_CTRL_shoulder", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")

    def create_ik_fk_switch_spine_controls(self):
        ik_fk_switch_offset, ik_fk_switch_ctrl = self.create_ik_fk_switch_spine_control(control_name="spine",
                                                                                        connected_limb="pelvis")
        cmds.parent(ik_fk_switch_offset, "spine_controls")


if __name__ == "__main__":
    pass
