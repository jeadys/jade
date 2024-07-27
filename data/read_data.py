import maya.cmds as cmds

from data.file_handler import get_open_file_name, read_data_from_file
from data.rig_structure import Module, Rig, Segment
from helpers.decorators.undoable_action import undoable_action
from ui.actions.build_module import add_default_module_attributes, add_default_rig_attributes, \
    add_default_segment_attributes
from ui.actions.refresh_ui import refresh_ui
from ui.widgets.combobox import node_combobox
from ui.widgets.tree_widget import tree_widget
from utilities.curve_from_locators import create_visual_connection


def import_rig_data():
    file_path: str = get_open_file_name()
    rig_data: dict = read_data_from_file(file_path)
    if rig_data:
        rig_instance = Rig.from_dict(rig_data)
        apply_rig_data(data=rig_instance)
        refresh_ui(tree=tree_widget, combobox=node_combobox)


@undoable_action
def apply_rig_data(data: Rig):
    if not cmds.objExists("master"):
        current_rig = cmds.createNode("network", name="master", skipSelect=True)
        add_default_rig_attributes(node=current_rig)

    for key, module in data.modules.items():
        apply_rig_module(module=module)
        apply_rig_segments(current_module=module.name, segments=module.segments)


def apply_rig_module(module: Module):
    if cmds.objExists(f"{module.name}"):
        return

    current_module = cmds.createNode("network", name=module.name, skipSelect=True)
    add_default_module_attributes(node=current_module, module=module)

    if module.parent_node:
        cmds.connectAttr(f"{module.parent_node}.children", f"{current_module}.parent_node")
    if module.parent_joint:
        cmds.connectAttr(f"{module.parent_joint}.children", f"{current_module}.parent_joint")


def apply_rig_segments(current_module: str, segments: list[Segment]):
    for index, segment in enumerate(segments):
        if cmds.objExists(f"{segment.name}"):
            continue

        current_segment = cmds.spaceLocator(name=segment.name)[0]
        add_default_segment_attributes(node=current_segment, segment=segment)

        if segment.parent_joint:
            cmds.parent(current_segment, segment.parent_joint)
            create_visual_connection(from_node=segment.parent_joint, to_node=current_segment)
            cmds.matchTransform(current_segment, segment.parent_joint, position=True, rotation=True, scale=False)

        cmds.move(segment.translateX, segment.translateY, segment.translateZ, current_segment,
                  relative=True, objectSpace=True)
        cmds.rotate(segment.rotateX, segment.rotateY, segment.rotateZ, current_segment,
                    relative=True, objectSpace=True)
        cmds.scale(segment.scaleX, segment.scaleY, segment.scaleZ, current_segment,
                   relative=True, objectSpace=True)

        cmds.connectAttr(f"{current_module}.segments{[index]}", f"{current_segment}.parent_node")
