# -*- coding: utf-8 -*-

import glob
import os
from orbis_eval.core import app


import logging
logger = logging.getLogger(__name__)


class Main(object):

    def __init__(self, rucksack, path=None):
        super(Main, self).__init__()
        self.rucksack = rucksack
        if not path:
            self.corpus_path = self.rucksack.open['config']['corpus_path']
        else:
            self.corpus_path = path

    def run(self):
        corpus = {}
        for file_dir in glob.glob(os.path.abspath(os.path.join(self.corpus_path, '*.txt'))):
            try:
                file_number = file_dir.split('/')[-1].split('.')[0]
                with open(file_dir) as open_file:
                    corpus[file_number] = open_file.read()
            except Exception as exception:
                logger.error(f"Corpus file empty: {file_dir} ({exception})")
        return corpus
