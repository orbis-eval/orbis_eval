# -*- coding: utf-8 -*-

import yaml
from configparser import SafeConfigParser


def load_config(config_files):
        configs = []

        for config_file in config_files:
            file_type = str(config_file).split(".")[-1]

            if file_type.lower() in ("yml", "yaml"):
                with open(config_file, 'r') as stream:
                    config = yaml.load(stream, Loader=yaml.SafeLoader)

            elif file_type.lower() in ("conf", "cfg", "ini"):
                config = SafeConfigParser(allow_no_value=True)
                config.read_string(config_file)

            else:
                return None

            config["file_name"] = str(config_file).split("/")[-1]
            config["file_dir"] = str(config_file).split("/")[0:-1]
            configs.append(config)

        return configs

