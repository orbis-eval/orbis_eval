# -*- coding: utf-8 -*-

import importlib
import pkgutil


def list_installed_addons() -> dict:

    orbis_addons = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith('orbis_addon_')
    }

    return orbis_addons


def load_addon(addon_name):

    module_name = f"orbis_addon_{addon_name}"

    orbis_addons = list_installed_addons()

    print(f"addons.py 25: {type(orbis_addons[module_name])}")
    return orbis_addons[module_name]
