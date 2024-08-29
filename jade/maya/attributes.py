import maya.cmds as cmds


def node_exists(func):
    def wrapper(node, *args, **kwargs):
        if not cmds.objExists(node):
            return cmds.warning(f"{node} doesn't exist")

        result = func(node, *args, **kwargs)
        return result

    return wrapper


def attribute_exists(func):
    def wrapper(node, attribute, *args, **kwargs):
        if not cmds.attributeQuery(attribute, node=node, exists=True):
            return cmds.warning(f"{attribute} doesn't exist on {node}")

        result = func(node, attribute, *args, **kwargs)
        return result

    return wrapper


@node_exists
@attribute_exists
def lock_attribute(node, attribute):
    attribute_name = f"{node}.{attribute}"
    cmds.setAttr(attribute_name, lock=True)


@node_exists
@attribute_exists
def unlock_attribute(node, attribute):
    attribute_name = f"{node}.{attribute}"
    cmds.setAttr(attribute_name, lock=False)

