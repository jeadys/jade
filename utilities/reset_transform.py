import maya.cmds as cmds


def reset_transforms():
    selection = cmds.ls(selection=True)

    for select in selection:
        cmds.setAttr(f"{select}.translate", 0, 0, 0)
        cmds.setAttr(f"{select}.rotate", 0, 0, 0)
        cmds.setAttr(f"{select}.scale", 1, 1, 1)
