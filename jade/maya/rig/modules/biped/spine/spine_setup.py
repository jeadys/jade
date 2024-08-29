from jade.maya.rig.meta_structure import Control, Module, Ribbon, Segment, Stretch, Twist
from jade.enums import Orient, RotateOrder, StretchMode


def create_chain_module(chain_amount, chain_name, max_distance=100):
    chain_module = Module(
        name=chain_name,
        module_type=chain_name,
        children=[""],
        segments=[],
        parent_node=None,
        parent_joint=None,
        twist=Twist(
            enabled=True,
            twist_joints=2,
            twist_influence=0.5
        ),
        stretch=Stretch(
            enabled=True,
            stretch_type=StretchMode.STRETCH,
            stretchiness=1,
            stretch_volume=0.5,
        ),
        ribbon=Ribbon(
            enabled=False,
            divisions=8,
            width=50,
            length=0.1,
            ribbon_controls=3,
            tweak_controls=2
        )
    )

    previous_segment = None

    distance_between = max_distance / (chain_amount - 1)

    for index in range(chain_amount):
        chain_item = Segment(
            name=f"{chain_name}_{index + 1}",
            translateX=0,
            translateY=distance_between if previous_segment else 0,
            translateZ=0,
            rotateX=0,
            rotateY=0,
            rotateZ=0,
            scaleX=1,
            scaleY=1,
            scaleZ=1,
            rotateOrder=RotateOrder.XYZ,
            orientation=Orient.WORLD if index == chain_amount - 1 else Orient.BONE,
            parent_node=chain_module.name,
            parent_joint=previous_segment.name if previous_segment else None,
            children=[],
            control=Control(
                name=f"{chain_name}_{index + 1}",
                parent_control=previous_segment.name if previous_segment else None,
            )
        )

        chain_module.segments.append(chain_item)

        # Update child_joint of the previous segment
        if previous_segment:
            previous_segment.children = chain_item.name

        previous_segment = chain_item  # Update previous_segment to the current Segment object

    return chain_module
