# -*- coding: utf-8 -*-

import importlib
import pkgutil


def load_plugin(pipeline_stage_name, plugin_name):

    if pipeline_stage_name in plugin_name and "orbis_plugin_" in plugin_name:
        module_name = plugin_name
    else:
        module_name = f"orbis_plugin_{pipeline_stage_name}_{plugin_name}"

    orbis_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith('orbis_plugin_')
    }

    return orbis_plugins[module_name]
