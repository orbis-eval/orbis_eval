import pkgutil


def get_installed_plugins():

    return sorted([module.name for module in pkgutil.iter_modules() if module.name.startswith('orbis_plugin')])
