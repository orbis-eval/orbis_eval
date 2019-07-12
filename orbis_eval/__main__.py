# -*- coding: utf-8 -*-

import configparser
import glob
import multiprocessing
import os
import yaml

from orbis_eval import app
from orbis_eval.core import pipeline
from orbis_eval.libs import maintainance
from orbis_eval.libs.arguments import parse_args
from orbis_plugin_aggregation_monocle import Main as monocle


def load_config(config_files) -> dict:
        configs = []
        for config_file in config_files:
            file_type = str(config_file).split(".")[-1]
            if file_type.lower() in ("yml", "yaml"):
                with open(config_file, 'r') as stream:
                    config = yaml.load(stream, Loader=yaml.SafeLoader)
            elif file_type.lower() in ("conf", "cfg", "ini"):
                config = configparser.ConfigParser(allow_no_value=True)
                config.read_string(config_file)
            else:
                return None
            config["file_name"] = str(config_file).split("/")[-1]
            config["file_dir"] = str(config_file).split("/")[0:-1]
            configs.append(config)
        app.logger.debug(f"test : {configs}")
        return configs


def start_runner(config):
    app.logger.debug("Starting pipeline")
    p = pipeline.Pipeline()
    p.load(config)
    p.run()


def run_orbis(config_file=None, args=None):

    app.logger.info("Welcome to Orbis!")

    if config_file:
        app.logger.debug("Single config")
        config = load_config([config_file])[0]
        monocle.check_resources(config, refresh=False)
        start_runner(config)

    else:
        app.logger.debug(f'Searching in: {str(os.path.join(app.paths.queue, "*.yaml"))}')
        config_files = sorted(glob.glob(os.path.join(app.paths.queue, "*.yaml")))
        app.logger.debug(f"Loading queue: {str(config_files)}")
        configs = load_config(config_files)
        monocle.check_resources(configs, refresh=False)

        if app.settings['multiprocessing']:
            with multiprocessing.Pool(processes=app.settings['multi_process_number']) as pool:
                pool.map(start_runner, configs)
        else:
            for config in configs:
                start_runner(config)


def run():
    args = parse_args()
    """
    # Seems to break logging... -_-
    app.logger.debug(f"Test {args.logging}")
    if args.logging:
        app.logger.setLevel(args.logging.upper())
    """
    if args and args.deletehtml:
        maintainance.delete_html_folders()
    if args.test:
        app.paths.queue = app.paths.test_queue

    # print(app.paths.test_queue)
    run_orbis(args.config or None, args)


if __name__ == '__main__':
    run()
