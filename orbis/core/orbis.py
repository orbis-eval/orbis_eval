"""Summary
"""
from orbis.config import paths
from orbis.config import settings
from orbis.lib import logger, files


class App(object):

    """Summary

    Attributes:
        filters (TYPE): Description
        lenses (TYPE): Description
        logger (TYPE): Description
        mappings (TYPE): Description
        paths (TYPE): Description
        root_path (TYPE): Description
    """

    def __init__(self):
        """Summary
        """

        # Getting paths
        self.paths = paths

        # Getting settings
        self.settings = settings

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

