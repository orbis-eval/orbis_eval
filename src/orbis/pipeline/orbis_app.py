#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import pathlib

from orbis.config import paths
from orbis.libs.logger_lib import create_logger
from orbis.libs.files_lib import create_folder


class App(object):
    """docstring for App"""

    def __init__(self):
        # Initialize settings
        self.root_path = paths.source_root
        self.paths = paths
        self.create_folders()
        
        # Initialize Logger
        self.logger = create_logger()

        # Initialize Resources
        self.lenses = None
        self.mappings = None
        self.filters = None

    def create_folders(self):
        pathlib.Path(self.paths.log_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.paths.output_path).mkdir(parents=True, exist_ok=True)
