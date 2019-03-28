#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-



import glob
import multiprocessing
import os
import shutil
from pprint import pprint

from orbis import app
from orbis.addons.satyanweshi import satyanweshi
from orbis.config import paths
from orbis.config import settings
from orbis.pipeline import runner
from orbis.libs import aggregation_lib
from orbis.libs import entity_preprocessing_lib
from orbis.libs import addon_lib


def start_orbis(args):
    """

    :param args:
    :return: None
    """

    if args.test:
        test_run()

    elif args.satyanweshi:
        satyanweshi.main(args)

    elif args.run_addon:
        addon_list = addon_lib.get_addons()

        if len(addon_list) > 0:
            addon = addon_lib.addon_selection(addon_list)
            addon.main()

        else:
            print("No addons installed.")
    else:
        run_orbis(args.config or None, args)


def start_runner(config):
    """

    :param config:
    :return:
    """

    runner_class = runner.Runner(config_yaml=config)
    runner_class.run()


def run_orbis(config=None, args=None):
    """

    :param config:
    :param args:
    :return:
    """

    app.logger.info("Welcome to Orbis!")

    if args and args.deletehtml:
        delete_html_folders()

    if config:
        entity_preprocessing_lib.check_resources(config, refresh=False)
        start_runner(config)

    else:
        configs = sorted(glob.glob(os.path.join(paths.evaluation_configs_dir, "*.yaml")))
        entity_preprocessing_lib.check_resources(configs, refresh=False)

        if settings.multiprocessing:
            with multiprocessing.Pool(processes=settings.multi_process_number) as pool:
                pool.map(start_runner, configs)
        else:
            for config in configs:
                start_runner(config)


def delete_html_folders():
    """

    :return:
    """
    for folder in os.listdir(paths.output_path):
        folder_path = os.path.abspath(os.path.join(paths.output_path, folder))
        if os.path.isdir(folder_path):
            shutil.rmtree(os.path.join(paths.output_path, folder))
            app.logger.info("Deleted: {}".format(folder_path))


def test_run():
    """

    :return:
    """
    text = """Microsoft is an American multinational corporation \
           headquartered in Redmond, Washington, that develops, \
           manufactures, licenses, supports and sells computer \
           software, consumer electronics and personal computers \
           and services. It was was founded by Bill Gates and \
           Paul Allen on April 4, 1975."""

    profile_name = "MAXIMUM.COVERAGE"
    output, err = aggregation_lib.run_recognize_api(text=text, profile_name=profile_name)

    print("\nOutput:")
    pprint(output)
    print("\n\nErrors: ")
    pprint(err)
