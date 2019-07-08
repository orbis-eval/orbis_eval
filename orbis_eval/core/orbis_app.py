# -*- coding: utf-8 -*-

import json
from distutils.dir_util import copy_tree
from pathlib import Path

from orbis_eval.config import paths
from orbis_eval.libs import logger, files


class App(object):

    def __init__(self):
        # Getting paths
        self.paths = paths

        self.settings = self.load_settings()
        self.user_folder()

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
        with open(self.paths.settings_file, 'r', encoding='utf-8') as settings_file:
            settings = json.load(settings_file)
        return settings

    def write_settings(self, user_dir, settings_dict):
        with open(self.paths.settings_file, 'r', encoding='utf-8') as settings_file:
            settings = json.load(settings_file)

        settings['user_dir'] = str(user_dir)
        settings.update(settings)
        with open(self.paths.settings_file, 'w', encoding='utf-8') as settings_file:
            json.dump(settings, settings_file, indent=4)

    def create_orbis_external_folder(self):
        default_dir = Path.home() / "orbis-eval"
        print("Where would you like to install the Orbis input/output directory?")
        user_dir = input(f"> ({str(default_dir)}):") or default_dir
        Path(user_dir).mkdir(parents=True, exist_ok=True)
        settings_dict = {'user_dir': str(user_dir)}
        self.write_settings(user_dir, settings_dict)
        return user_dir

    def fill_data(self, user_dir):
        source = Path("data")
        target = user_dir / "data"

        copy_tree(str(source), str(target))

    def fill_queue(self, user_dir):
        source = Path("queue")
        target = user_dir / "queue"
        copy_tree(str(source), str(target))

    def user_folder(self):
        if len(self.settings.get("user_dir", "")).strip() >= 0:
            user_dir = self.create_orbis_external_folder()
            self.fill_data(user_dir)
            self.fill_queue(user_dir)

