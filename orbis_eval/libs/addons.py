# -*- coding: utf-8 -*-

import importlib
import pkgutil


def list_installed_addons():

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

    return orbis_addons[module_name]
