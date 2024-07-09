import maya.cmds as cmds

from data.file_handler import get_save_file_name, save_data_to_file

from rig.components.arm import Rig, Module, Segment, Control


def export_rig_data():
    file_path: str = get_save_file_name()
    data: dict = retrieve_rig_data()
    rig_instance: Rig = Rig(name="Rig", description="An amazing rig ready to animate!", modules=data)
    save_data_to_file(file_path=file_path, data=rig_instance.to_json())


def retrieve_rig_data(blueprint="master", data=None):
    if not cmds.objExists(blueprint):
        return

    if data is None:
        data = {}

    modules = cmds.listConnections(f"{blueprint}.children") or []

    for module in modules:
        module_dict = Module(
            name=module,
            component_type=cmds.getAttr(f"{module}.component_type"),
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
                control=Control(
                    name=segment,
                    control_shape=None,
                    control_color=None,
                    control_scale=None,
                    parent_control=(cmds.listConnections(f"{segment}.parent_joint") or [None])[0],
                )
            )
            if cmds.attributeQuery("control_shape", node=segment, exists=True):
                segment_dict.control.control_shape = cmds.getAttr(f"{segment}.control_shape")
            if cmds.attributeQuery("control_color", node=segment, exists=True):
                segment_dict.control.control_color = cmds.getAttr(f"{segment}.control_color")
            if cmds.attributeQuery("control_scale", node=segment, exists=True):
                segment_dict.control.control_scale = cmds.getAttr(f"{segment}.control_scale")
            module_dict.segments.append(segment_dict)

        data[module] = module_dict

        retrieve_rig_data(blueprint=module, data=data)

    return data
