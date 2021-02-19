# -*- coding: utf-8 -*-

import glob
import multiprocessing
import os
import sys

import orbis_eval
from orbis_eval.core import app
from orbis_eval.core import pipeline
from orbis_eval.libs import maintainance
from orbis_eval.libs import config as config_module
from orbis_eval.libs.arguments import parse_args
from orbis_eval.plugins.aggregation.monocle import Main as monocle


import logging
logger = logging.getLogger(__name__)


def start_runner(config):
    logger.debug("Starting pipeline")
    p = pipeline.Pipeline()
    p.load(config)
    p.run()


def run_orbis(config_file=None, args=None, webgui=False):

    logger.info("Welcome to Orbis!")

    if config_file:
        logger.debug("Single config")
        config = config_module.load_config([config_file], webgui=webgui)[0]
        monocle.check_resources([config], refresh=False)
        start_runner(config)

    else:
        logger.debug(f'Searching in: {str(os.path.join(app.paths.queue, "*.yaml"))}')
        config_files = sorted(glob.glob(os.path.join(app.paths.queue, "*.yaml")))
        logger.debug(f"Loading queue: {str(config_files)}")
        configs = config_module.load_config(config_files, webgui=webgui)
        monocle.check_resources(configs, refresh=False)

        if len(config_files) <= 0:
            logger.error(
                f'\n\n'
                f'\tNo YAML Configuration files found!\n'
                f'\t---------------\n'
                f'\tPlease create one or more evaluation run YAML configuration files and save in "{app.paths.queue}"\n'
                f'\tor execute the YAML directly using the "--config" parameter:\n'
                f'\t\t"orbis-eval --config my_run.yaml"'
                f'\n\n'
            )
        else:
            if app.settings['multiprocessing']:
                logger.info(f">>>> multiprocessing {app.settings['multiprocessing']}")
                with multiprocessing.Pool(processes=app.settings['multi_process_number']) as pool:
                    pool.map(start_runner, configs)
            else:
                for config in configs:
                    start_runner(config)


def run():
    args = parse_args()
    """
    # Seems to break logging... -_-
    logger.debug(f"Test {args.logging}")
    if args.logging:
        logger.setLevel(args.logging.upper())
    """
    if args and args.version:
        print(f'Orbis version: {orbis_eval.__version__}')
        sys.exit(0)

    if args and args.deletehtml:
        maintainance.delete_html_folders()

    if args.test:
        app.paths.queue = app.paths.test_queue

    # print(app.paths.test_queue)
    run_orbis(args.config or None, args)


if __name__ == '__main__':
    run()
