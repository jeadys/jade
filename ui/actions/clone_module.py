import maya.cmds as cmds
from PySide2 import QtWidgets


def clone_module(item: QtWidgets.QTreeWidgetItem, original_prefix="", clone_prefix=""):
    module = item.text(0)
    parent_node = cmds.listConnections(f"{module}.parent_node")
    parent_joint = cmds.listConnections(f"{module}.parent_joint")
    segments = cmds.listConnections(f"{module}.segments")

    if parent_node:
        cmds.disconnectAttr(f"{parent_node[0]}.children", f"{module}.parent_node")

    if parent_joint:
        cmds.disconnectAttr(f"{parent_joint[0]}.children", f"{module}.parent_joint")

    dupe = cmds.duplicate(segments, returnRootsOnly=True, renameChildren=True, upstreamNodes=True,
                          inputConnections=False)

    cloned_module = cmds.listConnections(f"{dupe[0]}.parent_node")

    if parent_node:
        cmds.connectAttr(f"{parent_node[0]}.children", f"{module}.parent_node")
        cmds.connectAttr(f"{parent_node[0]}.children", f"{cloned_module[0]}.parent_node")

    if parent_joint:
        cmds.connectAttr(f"{parent_joint[0]}.children", f"{module}.parent_joint")
        cmds.connectAttr(f"{parent_joint[0]}.children", f"{cloned_module[0]}.parent_joint")

    rename_module(module=module, cloned_module=cloned_module[0], original_prefix=original_prefix,
                  clone_prefix=clone_prefix)


def rename_module(module, cloned_module, original_prefix, clone_prefix):
    module_renamed = cmds.rename(module, f"{original_prefix}{module}")
    cloned_module_renamed = cmds.rename(cloned_module, f"{clone_prefix}{module}")

    segments = cmds.listConnections(f"{module_renamed}.segments") or []
    cloned_segments = cmds.listConnections(f"{cloned_module_renamed}.segments") or []

    module_name, _, module_nr = module_renamed.rpartition("_")

    cmds.setAttr(f"{module_renamed}.side", original_prefix, type="string")
    cmds.setAttr(f"{cloned_module_renamed}.side", clone_prefix, type="string")

    cmds.setAttr(f"{module_renamed}.module_nr", module_nr, type="string")
    cmds.setAttr(f"{cloned_module_renamed}.module_nr", module_nr, type="string")

    for segment, cloned_segment in zip(segments, cloned_segments):
        segment_name, _, segment_nr = segment.rpartition("_")

        cmds.rename(segment, f"{original_prefix}{segment_name}_{module_nr}")
        cmds.rename(cloned_segment, f"{clone_prefix}{segment_name}_{module_nr}")

    children = cmds.listConnections(f"{module_renamed}.children") or []
    cloned_children = cmds.listConnections(f"{cloned_module_renamed}.children") or []

    rename_module_children(children, cloned_children, original_prefix, clone_prefix)


def rename_module_children(children, cloned_children, original_prefix, clone_prefix):
    for child, cloned_child in zip(children, cloned_children):
        child_renamed = cmds.rename(child, f"{original_prefix}{child}")
        cloned_child_renamed = cmds.rename(cloned_child, f"{clone_prefix}{child}")

        segments = cmds.listConnections(f"{child_renamed}.segments") or []
        cloned_segments = cmds.listConnections(f"{cloned_child_renamed}.segments") or []

        module_name, _, module_nr = child_renamed.rpartition("_")

        cmds.setAttr(f"{child_renamed}.side", original_prefix, type="string")
        cmds.setAttr(f"{cloned_child_renamed}.side", clone_prefix, type="string")

        cmds.setAttr(f"{child_renamed}.module_nr", module_nr, type="string")
        cmds.setAttr(f"{cloned_child_renamed}.module_nr", module_nr, type="string")

        for segment, cloned_segment in zip(segments, cloned_segments):
            segment_name, _, segment_nr = segment.rpartition("_")

            cmds.rename(segment, f"{original_prefix}{segment_name}_{module_nr}")
            cmds.rename(cloned_segment, f"{clone_prefix}{segment_name}_{module_nr}")

        child_children = cmds.listConnections(f"{child_renamed}.children") or []
        cloned_child_children = cmds.listConnections(f"{cloned_child_renamed}.children") or []

        rename_module_children(child_children, cloned_child_children, original_prefix, clone_prefix)


def remove_module(item: QtWidgets.QTreeWidgetItem):
    module = item.text(0)
    segments = cmds.listConnections(f"{module}.segments")
    if segments:
        cmds.delete(segments)
