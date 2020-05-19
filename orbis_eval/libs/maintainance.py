# -*- coding: utf-8 -*-

from orbis_eval.core import app

import os
import shutil
import logging
logger = logging.getLogger(__name__)


def delete_html_folders():
    for folder in os.listdir(app.paths.output_path):
        folder_path = os.path.abspath(os.path.join(app.paths.output_path, folder))
        if os.path.isdir(folder_path):
            shutil.rmtree(os.path.join(app.paths.output_path, folder))
            logger.info("Deleted: {}".format(folder_path))
