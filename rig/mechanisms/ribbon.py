import maya.cmds as cmds

from utilities.shapes import diamond_points, octagon_points


class Ribbon:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.side = cmds.getAttr(f"{self.node}.side")
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.prefix = f"{self.side}{self.name}_{self.module_nr}"

        self.nurbs_plane = None
        self.follicles = []
        self.intermediate_joints = []
        self.intermediate_groups = []
        self.tweak_joints = []

    def ribbon_plane(self, divisions, width, length):
        self.nurbs_plane = cmds.nurbsPlane(
            name=f"{self.prefix}_nurbsPlane",
            pivot=(0, 0, 0),
            axis=(0, 0, 1),
            width=width,
            lengthRatio=length,
            degree=3,
            patchesU=divisions,
            patchesV=1,
            constructionHistory=True
        )[0]

        plane_shape = cmds.listRelatives(self.nurbs_plane, children=True, shapes=True)

        step = 1 / divisions
        parameter_u = 0
        parameter_v = 0.5

        for x in range(divisions + 1):
            follicle_shape = cmds.createNode("follicle", name=f"{self.prefix}_follicle")
            follicle = cmds.listRelatives(follicle_shape, parent=True, type="transform")

            cmds.connectAttr(f"{follicle_shape}.outRotate", f"{follicle[0]}.rotate")
            cmds.connectAttr(f"{follicle_shape}.outTranslate", f"{follicle[0]}.translate")

            cmds.connectAttr(f"{plane_shape[0]}.local", f"{follicle_shape}.inputSurface")
            cmds.connectAttr(f"{plane_shape[0]}.worldMatrix", f"{follicle_shape}.inputWorldMatrix")

            cmds.setAttr(f"{follicle_shape}.parameterU", parameter_u)
            cmds.setAttr(f"{follicle_shape}.parameterV", parameter_v)
            parameter_u += step

            joint = cmds.joint(radius=1, name=f"{self.prefix}_ribbon_MCH_{x}")
            cmds.matchTransform(joint, follicle, position=True, rotation=False, scale=False)

            self.follicles.append(joint)

    def ribbon_intermediate_controls(self, control_amount=3):
        group_start = cmds.group(empty=True, name=f"{self.prefix}_ribbon_start_GROUP")
        cmds.select(deselect=True)
        joint_start = cmds.joint(name=f"{self.prefix}_ribbon_start")
        cmds.parent(joint_start, group_start)

        group_end = cmds.group(empty=True, name=f"{self.prefix}_ribbon_end_GROUP")
        cmds.select(deselect=True)
        joint_end = cmds.joint(name=f"{self.prefix}_ribbon_end")
        cmds.parent(joint_end, group_end)
        cmds.select(deselect=True)

        cmds.matchTransform(group_start, self.follicles[0], position=True, rotation=True, scale=False)
        cmds.matchTransform(group_end, self.follicles[-1], position=True, rotation=True, scale=False)

        self.intermediate_joints.append(joint_start)
        self.intermediate_groups.append(group_start)
        for i in range(1, control_amount + 1):
            joint_name = f"{self.prefix}_ribbon_{i}"
            group = cmds.group(empty=True, name=f'{self.prefix}_ribbon_GROUP_{i}')

            curve_control = cmds.curve(name=f"{self.prefix}_ribbon_control_{i}", pointWeight=octagon_points, degree=1)
            cmds.rotate(0, 0, -90, curve_control)
            cmds.scale(0.5, 0.5, 0.5, curve_control)
            cmds.makeIdentity(apply=True, scale=True, rotate=True)
            cmds.parent(curve_control, group)
            cmds.select(deselect=True)
            joint = cmds.joint(radius=2, name=joint_name)
            cmds.select(deselect=True)
            cmds.parent(joint, curve_control)

            constraint = cmds.pointConstraint([joint_start, joint_end], group, maintainOffset=False)[0]
            weight_b = i / (control_amount + 1)
            weight_a = 1.0 - weight_b

            cmds.setAttr(f"{constraint}.{joint_start}W0", weight_a)
            cmds.setAttr(f"{constraint}.{joint_end}W1", weight_b)

            self.intermediate_joints.append(joint)
            self.intermediate_groups.append(group)
            cmds.delete(constraint)

        self.intermediate_joints.append(joint_end)
        self.intermediate_groups.append(group_end)

    def ribbon_tweak_controls(self, control_amount=2):
        for i in range(len(self.intermediate_joints) - 1):
            start_joint = self.intermediate_joints[i]
            end_joint = self.intermediate_joints[i + 1]

            for j in range(1, control_amount + 1):
                joint_name = f"{self.prefix}_ribbon_TWEAK_{i}_{j}"

                group = cmds.group(empty=True, name=f"{self.prefix}_ribbon_TWEAK_GROUP_{i}_{j}")
                aim = cmds.group(empty=True, name=f"{self.prefix}_ribbon_TWEAK_AIM_{i}_{j}")
                cmds.parent(aim, group)

                curve_control = cmds.curve(name=f"{self.prefix}_ribbon_tweak_control_{i}_{j}",
                                           pointWeight=diamond_points, degree=1)
                cmds.rotate(0, 0, -90, curve_control)
                cmds.scale(0.5, 0.5, 0.5, curve_control)
                cmds.makeIdentity(apply=True, scale=True, rotate=True)
                cmds.parent(curve_control, aim)

                cmds.select(deselect=True)
                joint = cmds.joint(radius=2, name=joint_name)
                cmds.parent(joint, curve_control)

                constraint = cmds.pointConstraint([start_joint, end_joint], group, maintainOffset=False)[0]
                weight_end = j / (control_amount + 1)
                weight_start = 1.0 - weight_end

                cmds.setAttr(f"{constraint}.{start_joint}W0", weight_start)
                cmds.setAttr(f"{constraint}.{end_joint}W1", weight_end)

                cmds.aimConstraint(end_joint, aim,
                                   offset=(0, 0, 0),
                                   weight=1,
                                   aimVector=(1, 0, 0),
                                   upVector=(0, 1, 0),
                                   worldUpType="objectrotation",
                                   worldUpVector=(0, 1, 0),
                                   worldUpObject=start_joint)

                self.tweak_joints.append(joint)

    def attach_ribbon_to_module(self, segments):
        skinned_joints = self.intermediate_joints + self.tweak_joints
        cmds.skinCluster(skinned_joints, self.nurbs_plane, maximumInfluences=5, bindMethod=0, skinMethod=0)

        for segment, group in zip(segments, self.intermediate_groups):
            cmds.parentConstraint(f"{segment}_JNT", group, maintainOffset=False)

    def add_sine_deform(self, main_control):
        sine_nurbs = cmds.duplicate(self.nurbs_plane, name=f"{self.prefix}_sine_nurbsPlane")
        cmds.select(sine_nurbs)
        cmds.select(self.nurbs_plane, add=True)
        blend_shape = cmds.blendShape(name=f"blend_shape")

        cmds.select(sine_nurbs)
        sine = cmds.nonLinear(type="sine")
        cmds.rotate(0, 0, 90, sine)

        cmds.addAttr(main_control, niceName="sine_blend", longName="sine_blend", attributeType="float", keyable=True)
        cmds.addAttr(main_control, niceName="sine_amplitude", longName="sine_amplitude", attributeType="float",
                     keyable=True)
        cmds.addAttr(main_control, niceName="sine_wavelength", longName="sine_wavelength", attributeType="float",
                     keyable=True)
        cmds.addAttr(main_control, niceName="sine_orientation", longName="sine_orientation", attributeType="float",
                     keyable=True)
        cmds.addAttr(main_control, niceName="sine_offset", longName="sine_offset", attributeType="float", keyable=True)

        cmds.connectAttr(f"{main_control}.sine_blend", f"{blend_shape[0]}.{sine_nurbs[0]}")
        cmds.connectAttr(f"{main_control}.sine_amplitude", f"{sine[0]}.amplitude")
        cmds.connectAttr(f"{main_control}.sine_wavelength", f"{sine[0]}.wavelength")
        cmds.connectAttr(f"{main_control}.sine_orientation", f"{sine[1]}.rotateY")
        cmds.connectAttr(f"{main_control}.sine_offset", f"{sine[0]}.offset")

    def add_twist_deform(self, main_control):
        twist_nurbs = cmds.duplicate(self.nurbs_plane, name=f"{self.prefix}_twist_nurbsPlane")
        cmds.select(twist_nurbs)
        cmds.select(self.nurbs_plane, add=True)
        blend_shape = cmds.blendShape(name=f"blend_shape")

        cmds.select(twist_nurbs)
        twist = cmds.nonLinear(type="twist")
        cmds.rotate(0, 0, 90, twist)

        cmds.addAttr(main_control, niceName="twist_blend", longName="twist_blend", attributeType="float", keyable=True)
        cmds.addAttr(main_control, niceName="twist_offset", longName="twist_offset", attributeType="float",
                     keyable=True)

        cmds.connectAttr(f"{main_control}.twist_blend", f"{blend_shape[0]}.{twist_nurbs[0]}")
        cmds.connectAttr(f"{main_control}.twist_offset", f"{twist[0]}.startAngle")

# class UVPinAxis(int, Enum):
#     POSITIVE_X = 0
#     POSITIVE_Y = 1
#     POSITIVE_Z = 2
#     NEGATIVE_X = 3
#     NEGATIVE_Y = 4
#     NEGATIVE_Z = 5
#
#     def __int__(self) -> int:
#         return int.__int__(self)
#
#
# class UVPinOutput(int, Enum):
#     EXISTING_TRANSFORM = 0
#     NEW_TRANSFORM = 1
#     NEW_LOCATOR = 2
#     MATRIX = 3
#
#     def __int__(self) -> int:
#         return int.__int__(self)
#
#
# class Ribbon:
#
#     def __init__(self, node, name):
#         self.node = node
#         self.name = name
#         self.side = cmds.getAttr(f"{self.node}.side")
#         self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
#         self.prefix = f"{self.side}{self.name}_{self.module_nr}"
#         self.follicles = []
#         self.controls = []

# def create_ribbon_from_curves(self, start_curve, end_curve):
#     cmds.loft(start_curve, end_curve, constructionHistory=True, autoReverse=True, degree=3, sectionSpans=1,
#               range=True)

# def create_ribbon_plane(self, divisions, width, length):
#     plane = cmds.nurbsPlane(
#         pivot=(0, 0, 0),
#         axis=(0, 0, 1),
#         width=width,
#         lengthRatio=length,
#         degree=3,
#         patchesU=divisions,
#         patchesV=1,
#         constructionHistory=True
#     )[0]
#
#     plane_shape = cmds.listRelatives(plane, children=True, shapes=True)
#
#     step = 1 / divisions
#     parameter_u = 0
#     parameter_v = 0.5
#
#     for x in range(divisions + 1):
#         follicle_shape = cmds.createNode("follicle")
#         follicle = cmds.listRelatives(follicle_shape, parent=True, type="transform")
#
#         cmds.connectAttr(f"{follicle_shape}.outRotate", f"{follicle[0]}.rotate")
#         cmds.connectAttr(f"{follicle_shape}.outTranslate", f"{follicle[0]}.translate")
#
#         cmds.connectAttr(f"{plane_shape[0]}.local", f"{follicle_shape}.inputSurface")
#         cmds.connectAttr(f"{plane_shape[0]}.worldMatrix", f"{follicle_shape}.inputWorldMatrix")
#
#         cmds.setAttr(f"{follicle_shape}.parameterU", parameter_u)
#         cmds.setAttr(f"{follicle_shape}.parameterV", parameter_v)
#         parameter_u += step
#
#         joint = cmds.joint(radius=1, name=f"joint_{x}")
#         cmds.matchTransform(joint, follicle, position=True, rotation=False, scale=False)
#
#         self.follicles.append(joint)
#
#     control_amount = 5
#     control_step = width / (control_amount - 1)
#     control_start = 0

# for x in range(control_amount):
#     cmds.select(deselect=True)
#     joint_control = cmds.joint(radius=2, name=f"joint_control_{x}")
#     cmds.matchTransform(joint_control, self.follicles[0], position=True, rotation=True, scale=False)
#     cmds.move(control_start, 0, 0, relative=True, objectSpace=True)
#
#     control_start += control_step
#     curve_control = cmds.curve(name=f"curve_control_{x}", pointWeight=octagon_points, degree=1)
#     cmds.rotate(0, 0, -90, curve_control)
#     cmds.scale(0.2, 0.2, 0.2, curve_control)
#     cmds.makeIdentity(apply=True, scale=True, rotate=True)
#
#     cmds.matchTransform(curve_control, joint_control, position=True, rotation=True, scale=False)
#     cmds.parent(joint_control, curve_control)
#
#     bake_transform_to_offset_parent_matrix(joint_control)
#     bake_transform_to_offset_parent_matrix(curve_control)
#
#     self.controls.append(joint_control)
#
# cmds.skinCluster(*self.controls, plane, maximumInfluences=5, bindMethod=0, skinMethod=0)

# def create_uv_pin(self, name: str = None, components: list[int] | list[list[int]] = [0],
#                   tangent_axis=UVPinAxis.POSITIVE_Y,
#                   normal_axis: UVPinAxis = UVPinAxis.POSITIVE_X,
#                   uv_set: str = "map1", normalize_isoparms: bool = True, output: UVPinOutput = UVPinOutput.MATRIX,
#                   existing_transforms: list[str] = []):
#     """
#     This function creates uvPin-constrained Locators or Objects on specified objects and components with customized uvPin settings.
#     Parameters:
#         name (str): The name of the object.
#         components (list): Mesh objects (list of ints) or NURBS surface objects (list of lists: [[int, int]]).
#         tangent_axis (int): Tangent axis (0-5, where 0=X, 1=Y, 2=Z, 3=-X, 4=-Y, 5=-Z).
#         normal_axis (int): Normal axis (0-5, where 0=X, 1=Y, 2=Z, 3=-X, 4=-Y, 5=-Z).
#         uv_set (str): UV set name.
#         normalize_isoparms (bool): Whether to normalize isoparms.
#         output (int): Output type (0=Existing Transform, 1=New Transform, 2=New Locator, 3=Matrix).
#         existing_transforms (list): List of existing transforms (list of str).
#     """
#
#     # Check if there already is a shape origin node
#     shape_origin = None
#     shape = None
#     shapes = cmds.listRelatives(name, children=True, shapes=True)
#
#     if shapes:
#         for s in shapes:
#             io = cmds.getAttr(f"{s}.intermediateObject")
#             if io:
#                 shape_origin = s
#             else:
#                 shape = s
#     else:
#         raise cmds.error(f"No shapes found under the object {name}")
#
#     # Check if the shapes are the right type
#     shape_type = cmds.objectType(shapes[0])
#
#     # Defining attributes based on objectType
#     if shape_type == "mesh":
#         component_prefix = ".vtx"
#         component_attr = ".inMesh"
#         component_attr2 = ".worldMesh[0]"
#         component_attr3 = ".outMesh"
#     elif shape_type == "nurbsSurface":
#         component_prefix = ".cv"
#         component_attr = ".create"
#         component_attr2 = ".worldSpace[0]"
#         component_attr3 = ".local"
#         if len(components) == 1:
#             components = [[components[0], components[0]]]
#     else:
#         return cmds.error("Object provided needs to be Mesh or NURBS surface")
#
#         # Create shape origin if there isn't one
#     if shape_origin is None:
#         shape = shapes[0]
#         dup = cmds.duplicate(shape)
#         shape_origin = cmds.listRelatives(dup, children=True, shapes=True)
#         cmds.parent(shape_origin, name, shape=True, relative=True)
#         cmds.delete(dup)
#         shape_origin = cmds.rename(shape_origin, f"{shape}Orig")
#
#         # Check if inMesh attr has connection
#         in_connection = cmds.listConnections(f"{shape}{component_attr}", plugs=True, connections=True,
#                                              destination=True)
#         if in_connection:
#             cmds.connectAttr(in_connection[1], f"{shape_origin}{component_attr}")
#
#         cmds.connectAttr(f"{shape_origin}{component_attr2}", f"{shape}{component_attr}", force=True)
#         cmds.setAttr(f"{shape_origin}.intermediateObject", 1)
#
#     # Create uvPin Node
#     pin = cmds.createNode("uvPin", name=f"{name}_uvPin")
#
#     cmds.connectAttr(f"{shape}{component_attr2}", f"{pin}.deformedGeometry")
#     cmds.connectAttr(f"{shape_origin}{component_attr3}", f"{pin}.originalGeometry")
#
#     # create temporary readout node
#     if shape_type == "mesh":
#         readout = cmds.createNode("closestPointOnMesh")
#         cmds.connectAttr(f"{shape}.worldMesh[0]", f"{readout}.inMesh")
#
#     # Create and connect output
#     for i, component in enumerate(components):
#         if output == UVPinOutput.EXISTING_TRANSFORM and existing_transforms:
#             if i < len(existing_transforms):
#                 out = existing_transforms[i]
#                 cmds.xform(out, translation=(0, 0, 0), rotation=(0, 0, 0), worldSpace=True)
#                 cmds.connectAttr(f"{pin}.outputMatrix[{i}]", f"{out}.offsetParentMatrix")
#         elif output == UVPinOutput.NEW_TRANSFORM:
#             out = cmds.group(name=f"{name}_pinTransform_{i}", empty=True)
#             cmds.connectAttr(f"{pin}.outputMatrix[{i}]", f"{out}.offsetParentMatrix")
#         elif output == UVPinOutput.NEW_LOCATOR:
#             out = cmds.spaceLocator(name=f"{name}_pinLoc_{i}")[0]
#             cmds.connectAttr(f"{pin}.outputMatrix[{i}]", f"{out}.offsetParentMatrix")
#
#         if shape_type == "mesh":
#             pos = cmds.xform(f"{name}{component_prefix}[{components[i]}]", query=True, translation=True,
#                              worldSpace=True)
#
#             cmds.setAttr(f"{readout}.inPosition", pos[0], pos[1], pos[2])
#             parameter_u = cmds.getAttr(f"{readout}.parameterU")
#             parameter_v = cmds.getAttr(f"{readout}.parameterV")
#         else:
#             parameter_u, parameter_v = component
#
#         cmds.setAttr(f"{pin}.coordinate[{i}]", parameter_u, parameter_v)
#
#         if len(existing_transforms) > len(components) and output == UVPinOutput.EXISTING_TRANSFORM:
#             transforms = existing_transforms[len(components):]
#             for transform in transforms:
#                 i += 1
#                 cmds.xform(transform, translation=(0, 0, 0), rotation=(0, 0, 0), worldSpace=True)
#                 cmds.setAttr(f"{pin}.coordinate[{i}]", parameter_u, parameter_v)
#                 cmds.connectAttr(f"{pin}.outputMatrix[{i}]", f"{transform}.offsetParentMatrix")
#
#     # Set attributes
#     cmds.setAttr(f"{pin}.normalAxis", normal_axis)
#     cmds.setAttr(f"{pin}.tangentAxis", tangent_axis)
#     cmds.setAttr(f"{pin}.uvSetName", uv_set, type="string")
#     cmds.setAttr(f"{pin}.normalizedIsoParms", normalize_isoparms)
#
# create_uv_pin(name='nurbsPlane5', components=[[0, 0.5], [1, 0.5]], tangent_axis=UVPinAxis.POSITIVE_Y,
#               normal_axis=UVPinAxis.POSITIVE_X, uv_set="map1", normalize_isoparms=True,
#               output=UVPinOutput.NEW_LOCATOR, existing_transforms=[])
