from data.rig_structure import Control
from data.rig_structure import Module
from data.rig_structure import Segment
from utilities.enums import Color
from utilities.enums import Orient
from utilities.enums import RotateOrder
from utilities.enums import Shape


def create_chain_module(chain_amount, chain_name, max_distance=100):
    chain_module = Module(
        name=chain_name,
        component_type="chain",
        children=[""],
        segments=[],
        parent_node=None,
        parent_joint=None,
        mirror=False,
        stretch=True,
        twist=True,
        twist_joints=5,
        twist_influence=0.5
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
            orientation=Orient.BONE,
            parent_node=chain_module.name,
            parent_joint=previous_segment.name if previous_segment else None,
            children=[],
            control=Control(
                name=f"{chain_name}_{index + 1}",
                control_shape=Shape.CUBE,
                control_color=Color.GREEN,
                control_scale=5,
                parent_control=previous_segment.name if previous_segment else None,
            )
        )

        chain_module.segments.append(chain_item)

        # Update child_joint of the previous segment
        if previous_segment:
            previous_segment.children = chain_item.name

        previous_segment = chain_item  # Update previous_segment to the current Segment object

    return chain_module
