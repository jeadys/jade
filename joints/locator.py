import maya.cmds as cmds
from utilities.set_rgb_color import set_rgb_color


def create_locators(segments: list[str], positions: list[tuple]) -> list[str]:
    arm_locators_exist: bool = any(cmds.objExists(f"{locator}_LOC") for locator in segments)
    locator_parent_group: str = "locators"

    if arm_locators_exist:
        cmds.error(f"locators already exist in {locator_parent_group}.")

    if not cmds.objExists(locator_parent_group):
        cmds.group(empty=True, name=locator_parent_group)

    locators: list[str] = []
    previous_locator: str = locator_parent_group
    for index, (locator, position) in enumerate(zip(segments, positions)):
        current_locator: str = cmds.spaceLocator(name=f"{locator}_LOC")[0]
        set_rgb_color(node=current_locator, color=(1, 1, 0))

        cmds.move(*position, current_locator)
        cmds.parent(current_locator, previous_locator)

        locators.append(current_locator)
        previous_locator = current_locator

    return locators
