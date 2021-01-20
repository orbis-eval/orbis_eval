# -*- coding: utf-8 -*-

from .gold_type_detector import get_gold_file_handler

import logging
logger = logging.getLogger(__name__)


class Main(object):

    def __init__(self, rucksack, path=None):
        super(Main, self).__init__()
        self.rucksack = rucksack
        self.gold_path = path or self.rucksack.open['config']['gold_path']

    def run(self):
        return get_gold_file_handler(self.rucksack, self.gold_path).run()
