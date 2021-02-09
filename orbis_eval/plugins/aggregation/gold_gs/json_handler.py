import glob
import os
import gzip
from json import load

from .gold_file_handler import GoldFileHandler

import logging

logger = logging.getLogger(__name__)


class JsonHandler(GoldFileHandler):
    def __init__(self, rucksack, gold_path):
        super().__init__(rucksack, gold_path)

    def run(self):
        return self.get_gold_file()

    def get_gold_file(self):
        files = glob.glob(os.path.abspath(os.path.join(self.gold_path, '*.json.gz')))
        if len(files) == 1:
            with gzip.open(files[0], "r") as fgzip:
                return load(fgzip)
        else:
            raise FileNotFoundError(f'json.gz file not found in {self.gold_path}')
