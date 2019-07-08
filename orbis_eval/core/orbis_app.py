# -*- coding: utf-8 -*-

import json

from orbis_eval.config import paths
from orbis_eval.libs import logger, files


class App(object):

    def __init__(self):
        # Getting paths
        self.paths = paths

        # Load Settings
        self.settings = self.load_settings()

        # Initialize folders
        files.create_folders(self.paths)

        # Check if folders are available
        files.check_folders(self.paths)

        # Initialize logger
        self.logger = logger.create_logger(self)

        # Initialize Resources
        self.lenses = None
        self.mappings = None
        self.filters = None

    def load_settings(self):
        with open(self.paths.settings_file, 'r', encoding='utf-8') as open_file:
            settings = json.load(open_file)
        return settings
