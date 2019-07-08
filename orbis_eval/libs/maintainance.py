# -*- coding: utf-8 -*-

import os
import shutil

from orbis_eval import app


def delete_html_folders():
    for folder in os.listdir(app.paths.output_path):
        folder_path = os.path.abspath(os.path.join(paths.output_path, folder))
        if os.path.isdir(folder_path):
            shutil.rmtree(os.path.join(paths.output_path, folder))
            app.logger.info("Deleted: {}".format(folder_path))
