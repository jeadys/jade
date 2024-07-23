from typing import Literal

import maya.cmds as cmds

from data.rig_structure import Segment
from utilities.enums import Orient, RotateOrder


class Skeleton:

    def __init__(self, node):
        self.node = node
        self.side = cmds.getAttr(f"{self.node}.side")
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def generate_skeleton(self, segments: list[Segment]):
        skeleton_group = "skeleton"
        if not cmds.objExists(skeleton_group):
            cmds.group(empty=True, name=skeleton_group)

        for index, segment in enumerate(segments):
            if cmds.objExists(f"{segment}_JNT"):
                continue

            cmds.select(deselect=True)

            rotate_order = cmds.getAttr(f"{segment}.rotateOrder")
            current_segment = cmds.joint(name=f"{segment}_JNT", rotationOrder=RotateOrder(rotate_order).name)
            cmds.matchTransform(current_segment, segment, position=True, rotation=False, scale=False)

            parent_joint = cmds.listRelatives(segment, parent=True, shapes=False, type="transform")

            if index == 0 and self.selection:
                cmds.parent(current_segment, f"{self.selection[0]}_JNT")
            elif index == 0 and not self.selection:
                cmds.parent(current_segment, skeleton_group)
            elif parent_joint:
                cmds.parent(current_segment, f"{parent_joint[0]}_JNT")

    def orient_skeleton(self, segments: list[Segment]):
        for segment in segments:
            orientation = cmds.getAttr(f"{segment}.orientation")

            match orientation:
                case Orient.SKIP:
                    continue
                case Orient.WORLD:
                    cmds.joint(f"{segment}_JNT", edit=True, orientJoint="none",
                               zeroScaleOrient=True)
                case Orient.BONE:
                    cmds.joint(f"{segment}_JNT", edit=True, orientJoint="yzx",
                               secondaryAxisOrient="zup",
                               zeroScaleOrient=True)

            if self.side == "R_":
                cmds.rotate(180, 0, 0, f"{segment}_JNT.rotateAxis", relative=True, objectSpace=True)
