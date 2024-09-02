import sys

# if you have some packages that you often reload, you can put them here.
# And they will get reloaded if "packages" attribute is not explicitly stated
DEFAULT_RELOAD_PACKAGES = []


def unload_packages(silent=True, packages=None):
    if packages is None:
        packages = DEFAULT_RELOAD_PACKAGES

    # construct reload list
    reload_list = []
    for i in sys.modules.keys():
        for package in packages:
            if i.startswith(f"jade.{package}"):
                reload_list.append(i)

    # unload everything
    for i in reload_list:
        try:
            if sys.modules[i] is not None:
                del (sys.modules[i])
                if not silent:
                    print(f"Unloaded: {i}")
        except (Exception, ):
            print(f"Failed to unload: {i}")
