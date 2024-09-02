import maya.cmds as cmds

from data.file_handler import get_save_file_name, save_data_to_file
from jade.maya.rig.meta_structure import Control, Module, Ribbon, Rig, Segment, Stretch, Twist


def export_rig_data():
    file_path: str = get_save_file_name()
    data: dict = retrieve_rig_data()
    rig_instance: Rig = Rig(name="Rig", description="An amazing rig ready to animate!", modules=data)
    save_data_to_file(file_path=file_path, data=rig_instance.to_json())


def retrieve_rig_data(module="master", data=None):
    if not cmds.objExists(module):
        return

    if data is None:
        data = {}

    modules = cmds.listConnections(f"{module}.children") or []

    for module in modules:
        module_dict = Module(
            name=module,
            module_type=cmds.getAttr(f"{module}.module_type"),
            module_nr=cmds.getAttr(f"{module}.module_nr"),
            side=cmds.getAttr(f"{module}.side"),
            parent_node=(cmds.listConnections(f"{module}.parent_node") or [None])[0],
            parent_joint=(cmds.listConnections(f"{module}.parent_joint") or [None])[0],
            children=cmds.listConnections(f"{module}.children"),
            segments=[],
            twist=None,
            stretch=None,
            ribbon=None,
        )

        if cmds.attributeQuery("twist", node=module, exists=True):
            module_dict.twist = Twist(
                enabled=cmds.getAttr(f"{module}.twist_enabled"),
                twist_joints=cmds.getAttr(f"{module}.twist_joints"),
                twist_influence=0,
            )

        if cmds.attributeQuery("stretch", node=module, exists=True):
            module_dict.stretch = Stretch(
                enabled=cmds.getAttr(f"{module}.stretch_enabled"),
                stretchiness=0,
                stretch_volume=0,
                stretch_type=0,
            )

        if cmds.attributeQuery("ribbon", node=module, exists=True):
            module_dict.ribbon = Ribbon(
                enabled=cmds.getAttr(f"{module}.ribbon_enabled"),
                divisions=cmds.getAttr(f"{module}.ribbon_divisions"),
                width=cmds.getAttr(f"{module}.ribbon_width"),
                length=cmds.getAttr(f"{module}.ribbon_length"),
                ribbon_controls=cmds.getAttr(f"{module}.ribbon_controls"),
                tweak_controls=cmds.getAttr(f"{module}.tweak_controls"),
            )

        segments = cmds.listConnections(f"{module}.segments")

        for segment in segments:
            segment_dict = Segment(
                name=segment,
                translateX=cmds.getAttr(f"{segment}.translateX"),
                translateY=cmds.getAttr(f"{segment}.translateY"),
                translateZ=cmds.getAttr(f"{segment}.translateZ"),
                rotateX=cmds.getAttr(f"{segment}.rotateX"),
                rotateY=cmds.getAttr(f"{segment}.rotateY"),
                rotateZ=cmds.getAttr(f"{segment}.rotateZ"),
                scaleX=cmds.getAttr(f"{segment}.scaleX"),
                scaleY=cmds.getAttr(f"{segment}.scaleY"),
                scaleZ=cmds.getAttr(f"{segment}.scaleZ"),
                rotateOrder=cmds.getAttr(f"{segment}.rotateOrder"),
                orientation=cmds.getAttr(f"{segment}.orientation"),
                parent_node=(cmds.listConnections(f"{segment}.parent_node") or [None])[0],
                parent_joint=(cmds.listRelatives(segment, parent=True, shapes=False, type="transform") or [None])[0],
                children=cmds.listConnections(f"{segment}.children"),
                control=None
            )

            control = cmds.objExists(f"{segment}_FK_CTRL")
            if control:
                cvs = cmds.ls(f"{segment}_FK_CTRL.cv[*]", flatten=True)
                points = [cmds.xform(cv, query=True, objectSpace=True, translation=True) for cv in cvs]

                segment_dict.control = Control(
                    name=segment,
                    control_points=points,
                    control_rgb=(cmds.getAttr(f"{segment}_FK_CTRL.overrideColorRGB") or [None])[0],
                    parent_control=(cmds.listConnections(f"{segment}.parent_joint") or [None])[0],
                )

            module_dict.segments.append(segment_dict)

        data[module] = module_dict

        retrieve_rig_data(module=module, data=data)

    return data
