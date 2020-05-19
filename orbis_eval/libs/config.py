# -*- coding: utf-8 -*-

import yaml
from configparser import SafeConfigParser

import logging
logger = logging.getLogger(__name__)


def load_config(config_files, webgui=False) -> dict:

    configs = []
    if not webgui:
        for config_file in config_files:
            file_type = str(config_file).split(".")[-1]

            if file_type.lower() in ("yml", "yaml"):
                with open(config_file, 'r') as stream:
                    config = yaml.load(stream, Loader=yaml.SafeLoader)

            elif file_type.lower() in ("conf", "cfg", "ini"):
                config = SafeConfigParser(allow_no_value=True)
                config.read_string(config_file)

            else:
                pass

            config["file_name"] = str(config_file).split("/")[-1]
            config["file_dir"] = str(config_file).split("/")[0:-1]
            logger.info(f'Adding {config["file_name"]} to queue.')
            configs.append(config)
            logger.debug(f"test : {configs}")

    else:
        logger.debug(f"Loading Web Config")

        config = config_files[0]
        config["file_name"] = "webgui"
        config["file_dir"] = None
        configs.append(config)

    return configs
