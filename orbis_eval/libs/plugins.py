# -*- coding: utf-8 -*-

import importlib
import pkgutil
import os


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


def get_plugin_dir(file):
    plugin_dir = os.path.abspath("/".join(os.path.realpath(file).split("/")[:-2]))
    return plugin_dir


def catch_data(variable, function_name, file_name, file):
    plugin_dir = get_plugin_dir(file)

    data_dir = plugin_dir + "/tests/data/"

    with open(data_dir + function_name + "_" + file_name, "w") as open_file:
        open_file.write(str(variable))
