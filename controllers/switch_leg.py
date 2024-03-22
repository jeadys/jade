import maya.cmds as cmds
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape

reload(control_shape)


class SwitchLeg:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def create_ik_fk_switch_leg_control(self, control_name: str, connected_limb: str):
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
        cmds.matchTransform(ik_text_curve, f"{self.prefix}_SWITCH_CTRL_{control_name}",
                            position=True, rotation=False, scale=False)
        cmds.parent(ik_text_curve, ik_fk_switch_offset)

        fk_text_curve = ControlShape.curve_text(name=f"{self.prefix}_FK_TEXT_{control_name}_curve", text="FK")
        cmds.matchTransform(fk_text_curve, f"{self.prefix}_SWITCH_CTRL_{control_name}",
                            position=True, rotation=False, scale=False)
        cmds.parent(fk_text_curve, ik_fk_switch_offset)

        self.create_ik_fk_switch_leg_constraints(control_name=control_name, ik_fk_switch_ctrl=ik_fk_switch_ctrl)
        self.create_ik_fk_switch_leg_attribute_proxies(ik_fk_switch_ctrl=ik_fk_switch_ctrl)

        return ik_fk_switch_offset, ik_fk_switch_ctrl

    def create_ik_fk_switch_leg_constraints(self, control_name: str, ik_fk_switch_ctrl):
        reverse_node = cmds.createNode("reverse", name=f"{self.prefix}_IK_FK_SWITCH_{control_name}_REVERSED")

        # LEG IK SWITCH
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_DEF_femur_parentConstraint1.{self.prefix}_IK_femurW1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_DEF_tibia_parentConstraint1.{self.prefix}_IK_tibiaW1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_DEF_ankle_parentConstraint1.{self.prefix}_IK_ankleW1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_DEF_ball_parentConstraint1.{self.prefix}_IK_ballW1")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_DEF_ball_end_parentConstraint1.{self.prefix}_IK_ball_endW1")

        # hide/unhide IK leg controls
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{self.prefix}_IK_OFFSET_leg.visibility")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{self.prefix}_IK_OFFSET_knee.visibility")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                         f"{self.prefix}_IK_TEXT_{control_name}_curveShape.visibility")

        # Reverse IK >< FK switch
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{reverse_node}.inputX")

        # LEG FK SWITCH
        cmds.connectAttr(f"{reverse_node}.outputX",
                         f"{self.prefix}_DEF_femur_parentConstraint1.{self.prefix}_FK_femurW0")
        cmds.connectAttr(f"{reverse_node}.outputX",
                         f"{self.prefix}_DEF_tibia_parentConstraint1.{self.prefix}_FK_tibiaW0")
        cmds.connectAttr(f"{reverse_node}.outputX",
                         f"{self.prefix}_DEF_ankle_parentConstraint1.{self.prefix}_FK_ankleW0")
        cmds.connectAttr(f"{reverse_node}.outputX", f"{self.prefix}_DEF_ball_parentConstraint1.{self.prefix}_FK_ballW0")
        cmds.connectAttr(f"{reverse_node}.outputX",
                         f"{self.prefix}_DEF_ball_end_parentConstraint1.{self.prefix}_FK_ball_endW0")

        # hide/unhide FK leg controls
        cmds.connectAttr(f"{reverse_node}.outputX", f"{self.prefix}_FK_OFFSET_femur.visibility")
        cmds.connectAttr(f"{reverse_node}.outputX", f"{self.prefix}_FK_TEXT_{control_name}_curveShape.visibility")

    def create_ik_fk_switch_leg_attribute_proxies(self, ik_fk_switch_ctrl):
        # CONTROL IK FK SWITCH THROUGH FK CONTROLS ATTRIBUTE
        cmds.addAttr(f"{self.prefix}_FK_CTRL_femur", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_FK_CTRL_tibia", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_FK_CTRL_ankle", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_FK_CTRL_ball", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_FK_CTRL_ball_end", longName="IK_FK_SWITCH",
                     proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")

        # CONTROL IK FK SWITCH THROUGH IK CONTROLS ATTRIBUTE
        cmds.addAttr(f"{self.prefix}_IK_CTRL_leg", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_IK_CTRL_knee", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")

    def create_ik_fk_switch_leg_controls(self):
        ik_fk_switch_offset, ik_fk_switch_ctrl = self.create_ik_fk_switch_leg_control(control_name="leg", connected_limb="ankle")

        cmds.parent(ik_fk_switch_offset, f"{self.prefix}_leg_controls")


if __name__ == "__main__":
    pass
