#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

# Set the location of the folder containing the yaml test run files.
# paths start at the packege root (same level as setup.py)
# https://martin-thoma.com/configuration-files-in-python/
# https://docs.python.org/3/library/configparser.html

evaluation_configs_dir = None
multiprocessing = True
multi_process_number = 2
# logger_format = '%(asctime)s %(name)-5s %(module)-15s %(levelname)-12s %(message)s'
logger_format = '%(levelname)-8s %(asctime)-25s %(module)-25s %(lineno)-5d %(message)s'
logging_level = 'debug'
# Folders
default_folders_to_create = "log_path", "output_path"
