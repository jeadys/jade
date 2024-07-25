import maya.cmds as cmds

from utilities.shapes import diamond_points, octagon_points


follicles = []


def ribbon_plane(divisions, width, length):
    plane = cmds.nurbsPlane(
        pivot=(0, 0, 0),
        axis=(0, 0, 1),
        width=width,
        lengthRatio=length,
        degree=3,
        patchesU=divisions,
        patchesV=1,
        constructionHistory=True
    )[0]

    plane_shape = cmds.listRelatives(plane, children=True, shapes=True)

    step = 1 / divisions
    parameter_u = 0
    parameter_v = 0.5

    for x in range(divisions + 1):
        follicle_shape = cmds.createNode("follicle")
        follicle = cmds.listRelatives(follicle_shape, parent=True, type="transform")

        cmds.connectAttr(f"{follicle_shape}.outRotate", f"{follicle[0]}.rotate")
        cmds.connectAttr(f"{follicle_shape}.outTranslate", f"{follicle[0]}.translate")

        cmds.connectAttr(f"{plane_shape[0]}.local", f"{follicle_shape}.inputSurface")
        cmds.connectAttr(f"{plane_shape[0]}.worldMatrix", f"{follicle_shape}.inputWorldMatrix")

        cmds.setAttr(f"{follicle_shape}.parameterU", parameter_u)
        cmds.setAttr(f"{follicle_shape}.parameterV", parameter_v)
        parameter_u += step

        joint = cmds.joint(radius=1, name=f"joint_{x}")
        cmds.matchTransform(joint, follicle, position=True, rotation=False, scale=False)

        follicles.append(joint)

    return plane


intermediate_joints = []


def ribbon_intermediate_controls(control_amount=3):
    cmds.select(deselect=True)
    joint_start = cmds.joint(name="joint_start")
    cmds.select(deselect=True)
    joint_end = cmds.joint(name="joint_end")
    cmds.select(deselect=True)

    cmds.matchTransform(joint_start, follicles[0], position=True, rotation=True, scale=False)
    cmds.matchTransform(joint_end, follicles[-1], position=True, rotation=True, scale=False)

    intermediate_joints.append(joint_start)
    for i in range(1, control_amount + 1):
        joint_name = f'intermediate_joint_{i}'
        group = cmds.group(empty=True, name=f'intermediate_joint_group_{i}')

        curve_control = cmds.curve(name=f"curve_control_{i}", pointWeight=octagon_points, degree=1)
        cmds.rotate(0, 0, -90, curve_control)
        cmds.scale(0.5, 0.5, 0.5, curve_control)
        cmds.makeIdentity(apply=True, scale=True, rotate=True)
        cmds.parent(curve_control, group)
        cmds.select(deselect=True)
        joint = cmds.joint(radius=2, name=joint_name)
        cmds.select(deselect=True)
        cmds.parent(joint, curve_control)

        constraint = cmds.pointConstraint([joint_start, joint_end], group, mo=False)[0]
        weight_b = i / (control_amount + 1)
        weight_a = 1.0 - weight_b

        cmds.setAttr(f"{constraint}.{joint_start}W0", weight_a)
        cmds.setAttr(f"{constraint}.{joint_end}W1", weight_b)

        intermediate_joints.append(joint)
        cmds.delete(constraint)

    intermediate_joints.append(joint_end)


tweak_joints = []


def ribbon_tweak_controls(control_amount=2):
    for i in range(len(intermediate_joints) - 1):
        start_joint = intermediate_joints[i]
        end_joint = intermediate_joints[i + 1]

        for j in range(1, control_amount + 1):
            joint_name = f'tweak_joint_{i}_{j}'

            group = cmds.group(empty=True, name=f'tweak_joint_group_{i}_{j}')
            aim = cmds.group(empty=True, name=f'tweak_joint_aim_{i}_{j}')
            cmds.parent(aim, group)

            curve_control = cmds.curve(name=f"curve_control_{i}_{j}", pointWeight=diamond_points, degree=1)
            cmds.rotate(0, 0, -90, curve_control)
            cmds.scale(0.5, 0.5, 0.5, curve_control)
            cmds.makeIdentity(apply=True, scale=True, rotate=True)
            cmds.parent(curve_control, aim)

            cmds.select(deselect=True)
            joint = cmds.joint(radius=2, name=joint_name)
            cmds.parent(joint, curve_control)

            constraint = cmds.pointConstraint([start_joint, end_joint], group, mo=False)[0]
            weight_end = j / (control_amount + 1)
            weight_start = 1.0 - weight_end

            cmds.setAttr(f"{constraint}.{start_joint}W0", weight_start)
            cmds.setAttr(f"{constraint}.{end_joint}W1", weight_end)

            cmds.aimConstraint(end_joint, aim, offset=(0, 0, 0), weight=1, aimVector=(1, 0, 0),
                               upVector=(0, 1, 0), worldUpType="vector", worldUpVector=(0, 1, 0))

            tweak_joints.append(joint)


nurbs_plane = ribbon_plane(divisions=12, width=50, length=0.1)
ribbon_intermediate_controls(control_amount=3)
ribbon_tweak_controls(control_amount=2)
skinned_joints = intermediate_joints + tweak_joints
cmds.skinCluster(skinned_joints, nurbs_plane, maximumInfluences=5, bindMethod=0, skinMethod=0)
