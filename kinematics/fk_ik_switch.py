import maya.cmds as cmds

from utilities.curve import Curve


class FKIKSwitch:

    def __init__(self, prefix: str, name: str, ik_joints: list[str], fk_joints: list[str], ik_ctrls: list[str],
                 fk_ctrls: list[str]):
        self.prefix = prefix
        self.name = name
        self.attribute_name: str = f"{self.prefix}_{self.name}_IK_FK_SWITCH"
        self.ik_joints = ik_joints
        self.fk_joints = fk_joints
        self.ik_ctrls = ik_ctrls
        self.fk_ctrls = fk_ctrls
        self.control_shape: Curve = Curve()

    def create_ik_fk_switch_control(self):
        ik_fk_switch = "IK_FK_SWITCH"

        if not cmds.objExists(ik_fk_switch):
            cmds.group(empty=True, name="IK_FK_SWITCH")
            shape = self.control_shape.curve_text(name="switch_ctrl", text="FK/IK")
            cmds.parent(shape, ik_fk_switch)

        cmds.addAttr(
            ik_fk_switch, attributeType="float", niceName=self.attribute_name,
            longName=self.attribute_name, defaultValue=0, minValue=0, maxValue=1, keyable=True
        )

        self._create_ik_fk_switch_constraints(switch_ctrl=ik_fk_switch)
        self._create_ik_fk_switch_attribute_proxies(switch_ctrl=ik_fk_switch)

    def _create_ik_fk_switch_constraints(self, switch_ctrl: str):
        reverse_node = cmds.createNode("reverse", name=f"{self.prefix}_IK_FK_SWITCH_{self.name}_REVERSED")
        cmds.connectAttr(f"{switch_ctrl}.{self.attribute_name}", f"{reverse_node}.inputX")

        # IK switch
        for index, ik_joint in enumerate(self.ik_joints):
            cmds.connectAttr(f"{switch_ctrl}.{self.attribute_name}", f"{ik_joint[:-3]}_parentConstraint1.{ik_joint}W1")
            cmds.connectAttr(f"{switch_ctrl}.{self.attribute_name}", f"{ik_joint}.visibility")

        # hide/unhide IK controls
        for index, ctrl in enumerate(self.ik_ctrls):
            cmds.connectAttr(f"{switch_ctrl}.{self.attribute_name}", f"{ctrl}.visibility")

        # FK switch
        for index, fk_joint in enumerate(self.fk_joints):
            cmds.connectAttr(f"{reverse_node}.outputX", f"{fk_joint[:-3]}_parentConstraint1.{fk_joint}W0")
            cmds.connectAttr(f"{reverse_node}.outputX", f"{fk_joint}.visibility")

        # hide/unhide FK controls
        for index, ctrl in enumerate(self.fk_ctrls):
            cmds.connectAttr(f"{reverse_node}.outputX", f"{ctrl}.visibility")

    def _create_ik_fk_switch_attribute_proxies(self, switch_ctrl: str):
        for index, ctrl in enumerate(self.fk_ctrls):
            cmds.addAttr(ctrl, longName=self.attribute_name,
                         proxy=f"{switch_ctrl}.{self.attribute_name}")

        for index, ctrl in enumerate(self.ik_ctrls):
            cmds.addAttr(ctrl, longName=f"{self.attribute_name}",
                         proxy=f"{switch_ctrl}.{self.attribute_name}")
