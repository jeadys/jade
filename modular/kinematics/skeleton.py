import maya.cmds as cmds

from modular.biped.biped import Segment

from utilities.enums import Orient, RotateOrder

from typing import Literal


class Skeleton:

    def __init__(self, node, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def generate_skeleton(self):
        skeleton_group = "skeleton"
        if not cmds.objExists(skeleton_group):
            cmds.group(empty=True, name=skeleton_group)

        for segment in self.segments:
            if cmds.objExists(f"{self.prefix}{segment.name}_{self.blueprint_nr}_JNT"):
                continue

            cmds.select(deselect=True)
            current_segment = cmds.joint(name=f"{self.prefix}{segment.name}_{self.blueprint_nr}_JNT",
                                         rotationOrder=RotateOrder.YZX.name)

            cmds.matchTransform(current_segment, f"{segment.name}_{self.blueprint_nr}", position=True, rotation=False,
                                scale=False)
            if self.prefix == "R_":
                position = cmds.xform(current_segment, query=True, translation=True, worldSpace=True)
                cmds.move(position[0] * -1, current_segment, moveX=True, absolute=True, worldSpace=True)

            if segment.parent is not None:
                cmds.parent(current_segment, f"{self.prefix}{segment.parent.name}_{self.blueprint_nr}_JNT")
            elif segment.parent is None and self.selection:
                if cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
                    cmds.parent(current_segment, f"{self.prefix}{self.selection[0]}_JNT")
                else:
                    cmds.parent(current_segment, f"{self.selection[0]}_JNT")
            else:
                cmds.parent(current_segment, skeleton_group)

    def orient_skeleton(self):
        for segment in self.segments:
            match segment.orientation:
                case Orient.SKIP:
                    continue
                case Orient.WORLD:
                    cmds.joint(f"{self.prefix}{segment.name}_{self.blueprint_nr}_JNT", edit=True, orientJoint="none",
                               zeroScaleOrient=True)
                case Orient.BONE:
                    cmds.joint(f"{self.prefix}{segment.name}_{self.blueprint_nr}_JNT", edit=True, orientJoint="yzx",
                               secondaryAxisOrient="zup",
                               zeroScaleOrient=True)

            if self.prefix == "R_":
                cmds.rotate(180, 0, 0, f"{self.prefix}{segment.name}_{self.blueprint_nr}_JNT.rotateAxis", relative=True,
                            objectSpace=True)

    def order_skeleton(self):
        pass
