import maya.cmds as cmds
from utilities.curve import Curve
from importlib import reload
import utilities.curve as control_shape

reload(control_shape)


class ArmSwitch:
    def __init__(self, prefix) -> None:
        self.prefix = prefix
        self.arm_segments = [f"{self.prefix}_upperarm", f"{self.prefix}_lowerarm", f"{self.prefix}_wrist"]
        self.control_shape: Curve = Curve()

    def create_arm_switch(self):
        ik_fk_switch_offset, ik_fk_switch_ctrl = self.create_ik_fk_switch_leg_control(control_name="arm")
        cmds.parent(ik_fk_switch_offset, f"{self.prefix}_arm_controls")

    def create_ik_fk_switch_leg_control(self, control_name: str):
        ik_fk_switch_offset = cmds.group(empty=True, name=f"{self.prefix}_{control_name}")

        ik_fk_switch_ctrl = self.control_shape.curve_two_way_arrow(name=f"{self.prefix}_SWITCH_CTRL_{control_name}")
        cmds.addAttr(
            ik_fk_switch_ctrl, attributeType="float", niceName="IK_FK_SWITCH", longName="IK_FK_SWITCH", defaultValue=0, minValue=0, maxValue=1, keyable=True
        )

        cmds.setAttr(f"{ik_fk_switch_ctrl}.overrideEnabled", True)
        cmds.setAttr(f"{ik_fk_switch_ctrl}.overrideRGBColors", True)
        cmds.setAttr(f"{ik_fk_switch_ctrl}.overrideColorRGB", 1, 1, 0)

        cmds.parent(ik_fk_switch_ctrl, ik_fk_switch_offset)

        cmds.matchTransform(ik_fk_switch_offset, self.arm_segments[-1], position=True, rotation=False,
                            scale=False)
        position = cmds.xform(ik_fk_switch_offset, query=True, translation=True, worldSpace=True)
        cmds.move(position[0] * 1.75, position[1], position[2] - 25, ik_fk_switch_offset)
        cmds.pointConstraint(self.arm_segments[-1], ik_fk_switch_offset, maintainOffset=True)

        ik_text_curve = self.control_shape.curve_text(name=f"{self.prefix}_IK_TEXT_{control_name}_curve", text="IK")
        cmds.matchTransform(ik_text_curve, f"{self.prefix}_SWITCH_CTRL_{control_name}",
                            position=True, rotation=False, scale=False)
        cmds.parent(ik_text_curve, ik_fk_switch_offset)

        fk_text_curve = self.control_shape.curve_text(name=f"{self.prefix}_FK_TEXT_{control_name}_curve", text="FK")
        cmds.matchTransform(fk_text_curve, f"{self.prefix}_SWITCH_CTRL_{control_name}",
                            position=True, rotation=False, scale=False)
        cmds.parent(fk_text_curve, ik_fk_switch_offset)

        self.create_ik_fk_switch_leg_constraints(control_name=control_name, ik_fk_switch_ctrl=ik_fk_switch_ctrl)
        self.create_ik_fk_switch_leg_attribute_proxies(ik_fk_switch_ctrl=ik_fk_switch_ctrl)

        return ik_fk_switch_offset, ik_fk_switch_ctrl

    def create_ik_fk_switch_leg_constraints(self, control_name: str, ik_fk_switch_ctrl):
        reverse_node = cmds.createNode("reverse", name=f"{self.prefix}_IK_FK_SWITCH_{control_name}_REVERSED")

        for index, joint in enumerate(self.arm_segments):
            cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH",
                             f"{joint}_parentConstraint1.{joint}_IKW1")

        # hide/unhide IK leg controls
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{self.prefix}_arm_IK_CTRL.visibility")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{self.prefix}_elbow_IK_CTRL.visibility")
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{self.prefix}_IK_TEXT_{control_name}_curveShape.visibility")

        # Reverse IK >< FK switch
        cmds.connectAttr(f"{ik_fk_switch_ctrl}.IK_FK_SWITCH", f"{reverse_node}.inputX")

        # LEG FK SWITCH
        for index, joint in enumerate(self.arm_segments):
            cmds.connectAttr(f"{reverse_node}.outputX",
                             f"{joint}_parentConstraint1.{joint}_FKW0")

        # hide/unhide FK leg controls
        cmds.connectAttr(f"{reverse_node}.outputX", f"{self.arm_segments[0]}_FK_CTRL.visibility")
        cmds.connectAttr(f"{reverse_node}.outputX", f"{self.prefix}_FK_TEXT_{control_name}_curveShape.visibility")

    def create_ik_fk_switch_leg_attribute_proxies(self, ik_fk_switch_ctrl):
        # CONTROL IK FK SWITCH THROUGH FK CONTROLS ATTRIBUTE
        for index, joint in enumerate(self.arm_segments):
            cmds.addAttr(f"{joint}_FK_CTRL", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")

        # CONTROL IK FK SWITCH THROUGH IK CONTROLS ATTRIBUTE
        cmds.addAttr(f"{self.prefix}_arm_IK_CTRL", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")
        cmds.addAttr(f"{self.prefix}_elbow_IK_CTRL", longName="IK_FK_SWITCH", proxy=f"{ik_fk_switch_ctrl}.IK_FK_SWITCH")


if __name__ == "__main__":
    pass
