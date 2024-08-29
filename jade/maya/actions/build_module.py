import maya.cmds as cmds

from jade.decorators import undoable_chunk
from jade.enums import Orient
from jade.maya.colors import set_rgb_color
from jade.maya.rig.modules.biped.arm import arm_module
from jade.maya.rig.modules.biped.leg import leg_module
from jade.maya.rig.modules.biped.spine import create_chain_module
from jade.maya.rig.modules.creature.arachne_leg import arachne_leg_module
from jade.maya.rig.modules.creature.wing import wing_module
from jade.maya.rig.modules.quadruped.front_leg import front_leg_module
from jade.maya.rig.modules.quadruped.rear_leg import rear_leg_module
from jade.maya.shapes import get_shape


@undoable_chunk
def build_module(module):
    if not cmds.objExists("master"):
        current_rig = cmds.createNode("network", name="master", skipSelect=True)
        add_default_rig_attributes(node=current_rig)

    segments_dict = {"arm": arm_module, "leg": leg_module,
                     "spine": create_chain_module(chain_amount=5, chain_name="spine", max_distance=50),
                     "front_leg": front_leg_module, "rear_leg": rear_leg_module, "arachne_leg": arachne_leg_module,
                     "wing": wing_module}

    current_node = create_module_node(module=segments_dict[module])
    create_module_segments(node=current_node, module=segments_dict[module])


def create_module_node(module):
    current_module = cmds.createNode("network", name=f"{module.name}_module_#", skipSelect=True)
    add_default_module_attributes(node=current_module, module=module)

    cmds.connectAttr(f"master.children", f"{current_module}.parent_node")

    # selected_node = node_combobox.currentText()
    # selected_segment = segment_combobox.currentText()
    #
    # if selected_node:
    #     cmds.connectAttr(f"{selected_node}.children", f"{current_module}.parent_node")
    # if selected_segment:
    #     cmds.connectAttr(f"{selected_segment}.children", f"{current_module}.parent_joint")

    return current_module


def create_module_segments(node, module):
    module_nr = cmds.getAttr(f"{node}.module_nr")

    points = [(segment.translateX, segment.translateY, segment.translateZ) for segment in module.segments]

    curve = cmds.curve(name=f"{node}_curve", point=points, degree=1)
    curve_shape = get_shape(transform=curve)
    set_rgb_color(transform=curve, rgb=(1.0, 1.0, 1.0))

    for index, segment in enumerate(module.segments):
        current_segment = cmds.spaceLocator(name=f"{segment.name}_{module_nr}")[0]
        add_default_segment_attributes(node=current_segment, segment=segment)

        # selected_segment = segment_combobox.currentText()

        shape = cmds.listRelatives(current_segment, shapes=True, children=True)[0]
        cmds.connectAttr(f"{shape}.worldPosition[0]",
                         f"{curve_shape}.controlPoints[{len(module.segments) - (index + 1)}]")

        if segment.parent_joint:
            cmds.matchTransform(current_segment, f"{segment.parent_joint}_{module_nr}", position=True,
                                rotation=True, scale=False)
            cmds.move(segment.translateX, segment.translateY, segment.translateZ, current_segment, relative=True,
                      objectSpace=True)
            cmds.parent(current_segment, f"{segment.parent_joint}_{module_nr}")

        # elif not segment.parent_joint and selected_segment:
        #     cmds.matchTransform(current_segment, selected_segment, position=True, rotation=False, scale=False)
        #     cmds.parent(current_segment, selected_segment)
        #
        #     position = cmds.xform(query=True, translation=True, worldSpace=True)
        #     cmds.curve(curve, append=True, point=position)
        #     shape = cmds.listRelatives(selected_segment, shapes=True, children=True)[0]
        #     cmds.connectAttr(f"{shape}.worldPosition[0]", f"{curve_shape}.controlPoints[{len(module.segments)}]")

        cmds.rotate(segment.rotateX, segment.rotateY, segment.rotateZ, current_segment, relative=True, objectSpace=True)

        cmds.scale(segment.scaleX, segment.scaleY, segment.scaleZ, current_segment, relative=True, objectSpace=True)

        cmds.connectAttr(f"{node}.segments{[index]}", f"{current_segment}.parent_node")


def add_default_rig_attributes(node):
    cmds.addAttr(node, niceName="children", longName="children", attributeType="message")

    cmds.addAttr(node, niceName="module_type", longName="module_type", dataType="string", readable=False,
                 writable=False, hidden=True)

    cmds.setAttr(f"{node}.module_type", "master", type="string")


def add_default_module_attributes(node, module):
    cmds.addAttr(node, niceName="module_type", longName="module_type", dataType="string", readable=False,
                 writable=False, hidden=True)

    cmds.addAttr(node, niceName="module_nr", longName="module_nr", dataType="string", readable=True,
                 writable=True, hidden=False)

    cmds.addAttr(node, niceName="side", longName="side", dataType="string", readable=True, writable=True, hidden=False)

    cmds.addAttr(node, niceName="parent_node", longName="parent_node", attributeType="message", readable=False,
                 writable=True)

    cmds.addAttr(node, niceName="parent_joint", longName="parent_joint", attributeType="message")

    cmds.addAttr(node, niceName="children", longName="children", attributeType="message", readable=True, writable=False)

    cmds.addAttr(node, niceName="segments", longName="segments", attributeType="message", readable=True,
                 writable=True, multi=True, indexMatters=True)

    cmds.addAttr(node, niceName="is_built", longName="is_built", attributeType="bool", defaultValue=False,
                 readable=False, writable=False, hidden=True)

    cmds.setAttr(f"{node}.module_type", module.module_type, type="string")

    cmds.setAttr(f"{node}.module_nr", node.rsplit("_", 1)[-1], type="string")

    cmds.setAttr(f"{node}.side", module.side, type="string")

    if module.twist:
        cmds.addAttr(node, longName="twist", numberOfChildren=2, attributeType="compound")

        cmds.addAttr(node, niceName="twist_enabled", longName="twist_enabled", attributeType="bool",
                     defaultValue=module.twist.enabled, parent="twist")

        cmds.addAttr(node, niceName="twist_joints", longName="twist_joints", attributeType="long", minValue=1,
                     maxValue=5, defaultValue=module.twist.twist_joints, parent="twist")

    if module.stretch:
        cmds.addAttr(node, longName="stretch", numberOfChildren=1, attributeType="compound")

        cmds.addAttr(node, niceName="stretch_enabled", longName="stretch_enabled", attributeType="bool",
                     defaultValue=module.stretch.enabled, parent="stretch")

    if module.ribbon:
        cmds.addAttr(node, longName="ribbon", numberOfChildren=6, attributeType="compound")

        cmds.addAttr(node, niceName="ribbon_enabled", longName="ribbon_enabled", attributeType="bool",
                     defaultValue=module.ribbon.enabled, parent="ribbon")

        cmds.addAttr(node, niceName="ribbon_divisions", longName="ribbon_divisions", attributeType="long", minValue=1,
                     maxValue=20, defaultValue=module.ribbon.divisions, parent="ribbon")

        cmds.addAttr(node, niceName="ribbon_width", longName="ribbon_width", attributeType="double", minValue=1,
                     maxValue=100, defaultValue=module.ribbon.width, parent="ribbon")

        cmds.addAttr(node, niceName="ribbon_length", longName="ribbon_length", attributeType="double", minValue=0.1,
                     maxValue=1, defaultValue=module.ribbon.length, parent="ribbon")

        cmds.addAttr(node, niceName="ribbon_controls", longName="ribbon_controls", attributeType="long", minValue=1,
                     maxValue=5, defaultValue=module.ribbon.ribbon_controls, parent="ribbon")

        cmds.addAttr(node, niceName="tweak_controls", longName="tweak_controls", attributeType="long", minValue=0,
                     maxValue=5, defaultValue=module.ribbon.tweak_controls, parent="ribbon")


def add_default_segment_attributes(node, segment):
    cmds.addAttr(node, niceName="parent_node", longName="parent_node", attributeType="message",
                 readable=True, writable=True)

    cmds.addAttr(node, niceName="parent_joint", longName="parent_joint", attributeType="message",
                 readable=False, writable=True)

    cmds.addAttr(node, niceName="children", longName="children", attributeType="message",
                 readable=True, writable=False)

    cmds.addAttr(node, niceName="orientation", longName="orientation", attributeType="enum",
                 enumName=Orient.enum_to_string_attribute(), defaultValue=segment.orientation)

    cmds.setAttr(f"{node}.rotateOrder", segment.rotateOrder)

    if segment.control:
        cmds.addAttr(node, niceName="control_points", longName="control_points", dataType="pointArray")

        cmds.addAttr(node, niceName="control_rgb", longName="control_rgb", dataType="float3")

        cmds.setAttr(f"{node}.control_points", len(segment.control.control_points), *segment.control.control_points,
                     type="pointArray")
        cmds.setAttr(f"{node}.control_rgb", *segment.control.control_rgb, type="float3")
