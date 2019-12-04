# -*- coding: utf-8 -*-
"""Summary
"""

import json

from orbis_eval.config import paths
from orbis_eval.libs import logger, files


class App(object):

    """Summary

    Attributes:
        filters (TYPE): Description
        lenses (TYPE): Description
        logger (TYPE): Description
        mappings (TYPE): Description
        paths (TYPE): Description
        settings (TYPE): Description
    """

    def __init__(self):
        """Summary
        """
        # Getting paths
        self.paths = paths

        # Load Settings
        self.settings = self.load_settings()
        self.__name__ = "orbis-eval"

        # Initialize folders
        files.create_folders(self.paths)

        # Check if folders are available
        files.check_folders(self.paths)

        # Initialize logger
        self.logger = logger.create_logger(self)
        # self.logger = logger.create_logger(self, name=__name__)

        # self.app.logger.debug(f">>>>>>>>>>>>>>>>> {self.__name__}")

        # Initialize Resources
        self.lenses = None
        self.mappings = None
        self.filters = None

    def load_settings(self) -> dict:
        """Summary

        Returns:
            TYPE: Description
        """
        with open(self.paths.settings_file, 'r', encoding='utf-8') as open_file:
            settings = json.load(open_file)
        return settings
