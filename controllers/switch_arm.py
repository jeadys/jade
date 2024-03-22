import maya.cmds as cmds
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape

reload(control_shape)


class SwitchArm:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def create_ik_fk_switch_arm_control(self, control_name: str, connected_limb: str):
        ik_fk_switch_offset = cmds.group(empty=True, name=f"{self.prefix}_SWITCH_OFFSET_{control_name}")

        ik_fk_switch_ctrl = ControlShape.curve_double_arrow(name=f"{self.prefix}_SWITCH_CTRL_{control_name}")

        cmds.setAttr(f"{ik_fk_switch_ctrl}.overrideEnabled", 1)
        cmds.setAttr(f"{ik_fk_switch_ctrl}.overrideColor", 12)

        cmds.parent(ik_fk_switch_ctrl, ik_fk_switch_offset)

        cmds.matchTransform(ik_fk_switch_offset, f"{self.prefix}_DEF_{connected_limb}", position=True, rotation=False,
                            scale=False)
        position = cmds.xform(ik_fk_switch_offset, query=True, translation=True, worldSpace=True)
        cmds.move(position[0] * 1.75, position[1], position[2] - 25, ik_fk_switch_offset)
        cmds.addAttr(
            ik_fk_switch_ctrl, attributeType="float", niceName="IK_FK_SWITCH", longName="IK_FK_SWITCH", defaultValue=0,
            minValue=0, maxValue=1, keyable=True
        )

        ik_text_curve = ControlShape.curve_text(name=f"{self.prefix}_IK_TEXT_{control_name}_curve", text="IK")
        cmds.matchTransform(ik_text_curve, f"{self.prefix}_SWITCH_CTRL_{control_name}", position=True, rotation=False,
                            scale=False)
        cmds.parent(ik_text_curve, ik_fk_switch_offset)

        fk_text_curve = ControlShape.curve_text(name=f"{self.prefix}_FK_TEXT_{control_name}_curve", text="FK")
        cmds.matchTransform(fk_text_curve, f"{self.prefix}_SWITCH_CTRL_{control_name}", position=True, rotation=False,
                            scale=False)
        cmds.parent(fk_text_curve, ik_fk_switch_offset)

        self.create_ik_fk_switch_arm_constraints(control_name=control_name, ik_fk_switch_ctrl=ik_fk_switch_ctrl)
        self.create_ik_fk_switch_arm_attributes(ik_fk_switch_ctrl=ik_fk_switch_ctrl)

        return ik_fk_switch_offset, ik_fk_switch_ctrl

    def create_ik_fk_switch_arm_constraints(self, control_name: str, ik_fk_switch_ctrl):
        reverse_node = cmds.createNode("reverse", name=f"{self.prefix}_IK_FK_SWITCH_{control_name}_REVERSED")

        # ARM IK SWITCH
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_DEF_wrist_parentConstraint1.{self.prefix}_IK_wristW1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_DEF_radius_parentConstraint1.{self.prefix}_IK_radiusW1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_DEF_humerus_parentConstraint1.{self.prefix}_IK_humerusW1")

        # hide/unhide IK arm controls
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{self.prefix}_IK_OFFSET_arm.visibility")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{self.prefix}_IK_OFFSET_elbow.visibility")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_IK_TEXT_{control_name}_curveShape.visibility")

        # Only when the spine is created before the arms
        if cmds.objExists("FK_CTRL_spine_03") and cmds.objExists("IK_CTRL_shoulder"):
            cmds.connectAttr(f"SWITCH_CTRL_spine.IK_FK_SWITCH", f"L_arm_group_parentConstraint1.L_arm_group_IKW1")
            cmds.connectAttr(f"SWITCH_CTRL_spine.IK_FK_SWITCH",
                             f"L_FK_OFFSET_humerus_parentConstraint1.L_arm_group_IKW1")

        # Reverse IK >< FK switch
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{reverse_node}.inputX")

        # ARM FK SWITCH
        cmds.connectAttr(f"{reverse_node}.outputX",
                         f"{self.prefix}_DEF_wrist_parentConstraint1.{self.prefix}_FK_wristW0")
        cmds.connectAttr(f"{reverse_node}.outputX",
                         f"{self.prefix}_DEF_radius_parentConstraint1.{self.prefix}_FK_radiusW0")
        cmds.connectAttr(f"{reverse_node}.outputX",
                         f"{self.prefix}_DEF_humerus_parentConstraint1.{self.prefix}_FK_humerusW0")

        # hide/unhide FK arm controls
        cmds.connectAttr(f"{reverse_node}.outputX", f"{self.prefix}_FK_OFFSET_humerus.visibility")
        cmds.connectAttr(f"{reverse_node}.outputX", f"{self.prefix}_FK_TEXT_{control_name}_curveShape.visibility")

        # Only when the spine is created before the arms
        if cmds.objExists("FK_CTRL_spine_03") and cmds.objExists("IK_CTRL_shoulder"):
            cmds.connectAttr("IK_FK_SWITCH_spine_REVERSED.outputX", f"L_arm_group_parentConstraint1.L_arm_group_FKW0")
            cmds.connectAttr("IK_FK_SWITCH_spine_REVERSED.outputX",
                             f"L_FK_OFFSET_humerus_parentConstraint1.L_arm_group_FKW0")

    def create_ik_fk_switch_arm_attributes(self, ik_fk_switch_ctrl):
        # CONTROL IK FK SWITCH THROUGH FK CONTROLS ATTRIBUTE
        cmds.addAttr(f"{self.prefix}_FK_CTRL_humerus", longName="IK_FK_SWITCH",
                     proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_FK_CTRL_radius", longName="IK_FK_SWITCH",
                     proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_FK_CTRL_wrist", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")

        # CONTROL IK FK SWITCH THROUGH IK CONTROLS ATTRIBUTE
        cmds.addAttr(f"{self.prefix}_IK_CTRL_arm", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_IK_CTRL_elbow", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")

    def create_ik_fk_switch_arm_controls(self):
        ik_fk_switch_offset, ik_fk_switch_ctrl = self.create_ik_fk_switch_arm_control(control_name="arm",
                                                                                      connected_limb="wrist")
        cmds.parent(ik_fk_switch_offset, f"{self.prefix}_arm_controls")


if __name__ == "__main__":
    pass
