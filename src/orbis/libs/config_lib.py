#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import yaml


# Read yaml
def load_yaml_config(yaml_file=None):
    """

    :param yaml_file:
    :return:
    """
    with open(yaml_file, 'r') as stream:
        loaded_config = yaml.load(stream)
        loaded_config["file_name"] = str(yaml_file).split("/")[-1]
        loaded_config["file_dir"] = str(yaml_file).split("/")[0:-1]
    return loaded_config
