import maya.cmds as cmds

from data.file_handler import get_save_file_name, save_data_to_file
from data.rig_structure import Control, Module, Rig, Segment


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
            children=cmds.listConnections(f"{module}.children"),
            segments=[],
            parent_node=(cmds.listConnections(f"{module}.parent_node") or [None])[0],
            parent_joint=(cmds.listConnections(f"{module}.parent_joint") or [None])[0],
            mirror=cmds.getAttr(f"{module}.mirror"),
            stretch=cmds.getAttr(f"{module}.stretch"),
            twist=cmds.getAttr(f"{module}.twist"),
            twist_joints=cmds.getAttr(f"{module}.twist_joints"),
            twist_influence=cmds.getAttr(f"{module}.twist_influence")
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
                parent_joint=(cmds.listConnections(f"{segment}.parent_joint") or [None])[0],
                children=cmds.listConnections(f"{segment}.children"),
                control=None
            )

            control = cmds.objExists(f"L_{segment}_FK_CTRL")
            if control:
                cvs = cmds.ls(f"L_{segment}_FK_CTRL.cv[*]", flatten=True)
                points = [cmds.xform(cv, query=True, objectSpace=True, translation=True) for cv in cvs]

                segment_dict.control = Control(
                    name=segment,
                    control_shape=None,
                    control_color=None,
                    control_scale=None,
                    control_points=points,
                    control_rgb=(cmds.getAttr(f"L_{segment}_FK_CTRL.overrideColorRGB") or [None])[0],
                    parent_control=(cmds.listConnections(f"{segment}.parent_joint") or [None])[0],
                )

            module_dict.segments.append(segment_dict)

        data[module] = module_dict

        retrieve_rig_data(module=module, data=data)

    return data
