from typing import Literal

import maya.cmds as cmds

from data.rig_structure import Segment
from utilities.enums import Orient, RotateOrder


class Skeleton:

    def __init__(self, node, prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.prefix = prefix
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def generate_skeleton(self, segments: list[Segment]):
        skeleton_group = "skeleton"
        if not cmds.objExists(skeleton_group):
            cmds.group(empty=True, name=skeleton_group)

        for segment in segments:
            if cmds.objExists(f"{self.prefix}{segment}_JNT"):
                continue

            cmds.select(deselect=True)

            current_segment = cmds.joint(name=f"{self.prefix}{segment}_JNT", rotationOrder=RotateOrder.YZX.name)
            cmds.matchTransform(current_segment, segment, position=True, rotation=False, scale=False)

            if self.prefix == "R_":
                position = cmds.xform(current_segment, query=True, translation=True, worldSpace=True)
                cmds.move(position[0] * -1, current_segment, moveX=True, absolute=True, worldSpace=True)

            parent_joint = cmds.listConnections(f"{segment}.parent_joint")

            if parent_joint is not None:
                cmds.parent(current_segment, f"{self.prefix}{parent_joint[0]}_JNT")
            elif parent_joint is None and self.selection:
                if cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
                    cmds.parent(current_segment, f"{self.prefix}{self.selection[0]}_JNT")
                else:
                    cmds.parent(current_segment, f"{self.selection[0]}_JNT")
            else:
                cmds.parent(current_segment, skeleton_group)

    def orient_skeleton(self, segments: list[Segment]):
        for segment in segments:
            orientation = cmds.getAttr(f"{segment}.orientation")

            match orientation:
                case Orient.SKIP:
                    continue
                case Orient.WORLD:
                    cmds.joint(f"{self.prefix}{segment}_JNT", edit=True, orientJoint="none",
                               zeroScaleOrient=True)
                case Orient.BONE:
                    cmds.joint(f"{self.prefix}{segment}_JNT", edit=True, orientJoint="yzx",
                               secondaryAxisOrient="zup",
                               zeroScaleOrient=True)

            if self.prefix == "R_":
                cmds.rotate(180, 0, 0, f"{self.prefix}{segment}_JNT.rotateAxis", relative=True,
                            objectSpace=True)
