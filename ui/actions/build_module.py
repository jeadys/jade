import maya.cmds as cmds
from PySide2 import QtWidgets

from helpers.decorators.undoable_action import undoable_action
from rig.modules.biped.arm import arm_module
from rig.modules.biped.leg import leg_module
from rig.modules.biped.spine import create_chain_module
from rig.modules.creature.arachne_leg import arachne_leg_module
from rig.modules.creature.wing import wing_module
from rig.modules.quadruped.front_leg import front_leg_module
from rig.modules.quadruped.rear_leg import rear_leg_module
from ui.actions.tree_view import node_combobox, segment_combobox, StandardItem, tree_view
from utilities.curve_from_locators import create_visual_connection
from utilities.enums import Color, Orient, Shape


# from rig.modules.creature.wing import wing_segments


def update_driven_combobox(driver_combobox: QtWidgets.QComboBox, driven_combobox: QtWidgets.QComboBox, attribute: str):
    selected_item = driver_combobox.currentText()
    has_attribute = cmds.attributeQuery(attribute, node=selected_item, exists=True)
    retrieved_items = cmds.listConnections(f"{selected_item}.{attribute}") if has_attribute else []
    driven_combobox.clear()
    driven_combobox.addItems(retrieved_items)


node_combobox.currentIndexChanged.connect(
    lambda val: update_driven_combobox(driver_combobox=node_combobox, driven_combobox=segment_combobox,
                                       attribute="segments"))


@undoable_action
def build_module(module_component):
    if not cmds.objExists("master"):
        cmds.createNode("network", name="master", skipSelect=True)
        cmds.addAttr("master", niceName="children", longName="children", attributeType="message")
        cmds.addAttr("master", niceName="module_type", longName="module_type", dataType="string", readable=False,
                     writable=False, hidden=True)
        cmds.setAttr("master.module_type", "master", type="string")

    segments_dict = {"arm": arm_module, "leg": leg_module,
                     "spine": create_chain_module(chain_amount=5, chain_name="spine"), "front_leg": front_leg_module,
                     "rear_leg": rear_leg_module, "arachne_leg": arachne_leg_module, "wing": wing_module}

    current_node = create_module_node(module=segments_dict[module_component])
    create_module_segments(node=current_node, module=segments_dict[module_component])


def create_module_node(module):
    current_module = cmds.createNode("network", name=f"{module.name}_module_#", skipSelect=True)

    add_default_node_attributes(node=current_module)
    cmds.setAttr(f"{current_module}.module_type", module.module_type, type="string")
    cmds.setAttr(f"{current_module}.module_nr", current_module.rsplit("_", 1)[-1], type="string")
    cmds.setAttr(f"{current_module}.mirror", module.mirror)
    cmds.setAttr(f"{current_module}.stretch", module.stretch)
    cmds.setAttr(f"{current_module}.twist", module.twist)
    cmds.setAttr(f"{current_module}.twist_joints", module.twist_joints)
    cmds.setAttr(f"{current_module}.twist_influence", module.twist_influence)

    selected_node = node_combobox.currentText()
    selected_segment = segment_combobox.currentText()

    if selected_segment:
        cmds.connectAttr(f"{selected_segment}.children", f"{current_module}.parent_joint")

    if selected_node:
        cmds.connectAttr(f"{selected_node}.children", f"{current_module}.parent_node")

    root_item = StandardItem(current_module, font_size=12)
    tree_view.add_item(name=current_module, item=root_item, parent_name=selected_node)
    node_combobox.addItem(current_module)

    return current_module


def create_module_segments(node, module):
    module_nr = cmds.getAttr(f"{node}.module_nr")
    for index, segment in enumerate(module.segments):
        current_segment = cmds.spaceLocator(name=f"{segment.name}_{module_nr}")[0]
        add_default_segment_attributes(segment=current_segment)
        cmds.setAttr(f"{current_segment}.control_shape", segment.control.control_shape)
        cmds.setAttr(f"{current_segment}.control_color", segment.control.control_color)
        cmds.setAttr(f"{current_segment}.control_scale", segment.control.control_scale)
        cmds.setAttr(f"{current_segment}.orientation", segment.orientation)
        cmds.setAttr(f"{current_segment}.rotateOrder", segment.rotateOrder)

        selected_segment = segment_combobox.currentText()

        if segment.parent_joint:
            cmds.matchTransform(current_segment, f"{segment.parent_joint}_{module_nr}", position=True,
                                rotation=True, scale=False)
            cmds.move(segment.translateX, segment.translateY, segment.translateZ, current_segment, relative=True,
                      objectSpace=True)
            cmds.parent(current_segment, f"{segment.parent_joint}_{module_nr}")
            cmds.connectAttr(f"{segment.parent_joint}_{module_nr}.children", f"{current_segment}.parent_joint")
            create_visual_connection(from_node=f"{segment.parent_joint}_{module_nr}", to_node=current_segment)

        elif not segment.parent_joint and selected_segment:
            cmds.matchTransform(current_segment, selected_segment, position=True, rotation=False, scale=False)
            cmds.parent(current_segment, selected_segment)
            cmds.connectAttr(f"{selected_segment}.children", f"{current_segment}.parent_joint")
            create_visual_connection(from_node=selected_segment, to_node=current_segment)

        cmds.rotate(segment.rotateX, segment.rotateY, segment.rotateZ, current_segment, relative=True,
                    objectSpace=True)

        cmds.scale(segment.scaleX, segment.scaleY, segment.scaleZ, current_segment, relative=True,
                   objectSpace=True)

        cmds.connectAttr(f"{node}.segments{[index]}", f"{current_segment}.parent_node")


def add_default_node_attributes(node):
    cmds.addAttr(node, niceName="module_type", longName="module_type", dataType="string", readable=False,
                 writable=False, hidden=True)
    cmds.addAttr(node, niceName="module_nr", longName="module_nr", dataType="string", readable=False,
                 writable=False, hidden=True)
    cmds.addAttr(node, niceName="parent_node", longName="parent_node", attributeType="message", readable=False,
                 writable=True)
    cmds.addAttr(node, niceName="parent_joint", longName="parent_joint", attributeType="message")
    cmds.addAttr(node, niceName="mirror", longName="mirror", attributeType="bool", defaultValue=1)

    cmds.addAttr(node, niceName="stretch", longName="stretch", attributeType="bool", defaultValue=1)
    cmds.addAttr(node, niceName="twist", longName="twist", attributeType="bool", defaultValue=1)
    cmds.addAttr(node, niceName="twist_joints", longName="twist_joints", attributeType="long", minValue=1,
                 maxValue=10, defaultValue=5)
    cmds.addAttr(node, niceName="twist_influence", longName="twist_influence", attributeType="double", minValue=0,
                 maxValue=1, defaultValue=0.75)

    cmds.addAttr(node, niceName="children", longName="children", attributeType="message", readable=True,
                 writable=False)
    cmds.addAttr(node, niceName="segments", longName="segments", attributeType="message", readable=True,
                 writable=True, multi=True, indexMatters=True)

    cmds.addAttr(node, niceName="is_built", longName="is_built", attributeType="bool", defaultValue=False,
                 readable=False, writable=False, hidden=True)


def add_default_segment_attributes(segment):
    cmds.addAttr(segment, niceName="parent_node", longName="parent_node", attributeType="message",
                 readable=True, writable=True)
    cmds.addAttr(segment, niceName="parent_joint", longName="parent_joint", attributeType="message",
                 readable=False, writable=True)
    cmds.addAttr(segment, niceName="children", longName="children", attributeType="message",
                 readable=True, writable=False)

    cmds.addAttr(segment, niceName="control_shape", longName="control_shape", attributeType="enum",
                 enumName=Shape.enum_to_string_attribute(), defaultValue=0)
    cmds.addAttr(segment, niceName="control_color", longName="control_color", attributeType="enum",
                 enumName=Color.enum_to_string_attribute(), defaultValue=0)
    cmds.addAttr(segment, niceName="control_scale", longName="control_scale", attributeType="float", minValue=1,
                 maxValue=10, defaultValue=1)
    cmds.addAttr(segment, niceName="orientation", longName="orientation", attributeType="enum",
                 enumName=Orient.enum_to_string_attribute(), defaultValue=0)
