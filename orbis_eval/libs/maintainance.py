# -*- coding: utf-8 -*-

from orbis_eval.core import app

import shutil
import logging
logger = logging.getLogger(__name__)


def delete_html_folders():
    for folder in app.paths.output_path.iterdir():
        folder_path = app.paths.output_path / folder
        if folder_path.is_dir():
            shutil.rmtree(folder_path)
            logger.info("Deleted: {}".format(folder_path))
