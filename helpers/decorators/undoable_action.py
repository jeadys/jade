import maya.cmds as cmds


def undoable_action(func):
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            result = func(*args, **kwargs)
            cmds.select(deselect=True)
        finally:
            cmds.undoInfo(closeChunk=True)
        return result

    return wrapper
