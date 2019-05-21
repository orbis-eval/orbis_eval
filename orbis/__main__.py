"""Summary
"""
import glob
import multiprocessing
import os
import yaml
import configparser

from orbis import app
from orbis.core import pipeline
from orbis.plugins.aggregation.monocle.main import check_resources
from orbis.lib import addons
from orbis.lib import maintainance
from orbis.interfaces import webgui
from orbis.lib.arguments import parse_args


def load_config(config_files) -> dict:
        """Summary

        Returns:
            dict: Description

        Args:
            config_files (TYPE): Description
        """
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
        return configs


def start_runner(config):
    """Summary

    Args:
        config (TYPE): Description
    """
    app.logger.debug("Starting pipeline")
    p = pipeline.Pipeline()
    p.load(config)
    p.run()


def run_orbis(config_file=None, args=None):
    """Summary

    Args:
        config_file (None, optional): Description
        args (None, optional): Description
    """
    app.logger.info("Welcome to Orbis!")

    if config_file:
        app.logger.debug("Single config")
        config = load_config([config_file])[0]
        check_resources(config, refresh=False)
        start_runner(config)

    else:
        config_files = sorted(glob.glob(os.path.join(app.paths.queue, "*.yaml")))
        app.logger.debug(f"Loading queue: {str(config_files)}")

        configs = load_config(config_files)
        check_resources(configs, refresh=False)

        if app.settings.multiprocessing:
            with multiprocessing.Pool(processes=app.settings.multi_process_number) as pool:
                pool.map(start_runner, configs)
        else:
            for config in configs:
                start_runner(config)


def main():
    """Summary
    """
    args = parse_args()

    if args and args.deletehtml:
        maintainance.delete_html_folders()

    if args.test:
        app.paths.queue = app.paths.test_queue

    if args.start_server:
        webgui.server.start()
    elif args.run_addon:
        addon_list = addons.get_addons()
        if len(addon_list) > 0:
            addon = addons.addon_selection(addon_list)
            addon.main()
        else:
            print("No addons installed.")
    else:
        run_orbis(args.config or None, args)


if __name__ == '__main__':
    main()
