# -*- coding: utf-8 -*-

import datetime

"""
import sys
print('\n'.join(sys.path))
"""
# print(imp.find_module("orbis_eval/main"))

from orbis_eval.core import app
from orbis_eval.core.rucksack import Rucksack
from orbis_eval.libs.files import save_rucksack
from orbis_eval.libs.plugins import load_plugin
from orbis_eval.plugins.aggregation.serial_corpus import Main as SerialCorpus
from orbis_eval.plugins.aggregation.gold_gs import Main as GoldGS

import logging

logger = logging.getLogger(__name__)
timestamp = "{:%Y-%m-%d_%H:%M:%S.%f}".format(datetime.datetime.now())


class Pipeline(object):

    def __init__(self):
        super(Pipeline, self).__init__()

    def load(self, config):
        self.rucksack = Rucksack(config)
        self.file_name = self.rucksack.open['config']['file_name']

    def get_plugin(self, pipeline_stage_name, plugin_name):

        logger.debug(f"Getting {pipeline_stage_name} plugin: {plugin_name}")

        imported_module = load_plugin(pipeline_stage_name, plugin_name)
        module_class_object = imported_module.Main
        return module_class_object

    @classmethod
    def run_plugin(cls, pipeline_stage_name, plugin_name, rucksack):
        logger.debug(f"Running {pipeline_stage_name} plugin: {plugin_name}")
        plugin = cls.get_plugin(cls, pipeline_stage_name, plugin_name)
        rucksack = plugin(rucksack).run()
        return rucksack

    def run(self):
        logger.info(f"Running: {self.file_name}")

        # Aggregation
        logger.info(f"Starting aggregation for {self.file_name}")
        self.rucksack = Aggregation(self.rucksack).run()

        if not self.rucksack:
            return False

        # Evaluation
        if self.rucksack.open['config']['evaluation']['name']:
            logger.info(f"Starting evaluation for {self.file_name}")
            self.rucksack = Evaluation(self.rucksack).run()

            if not self.rucksack:
                return False
        else:
            logger.info("Skip evaluation step. No evaluation defined.")

        save_rucksack(f"{app.paths.log_path}/results/{self.file_name}-{timestamp}",
                      self.rucksack, timestamp)

        # Storage
        logger.info(f"Starting storage for {self.file_name}")
        self.rucksack = Storage(self.rucksack).run()

        return self.rucksack


###############################################################################
class Aggregation(Pipeline):

    def __init__(self, rucksack):
        super(Aggregation, self).__init__()
        self.pipeline_stage_name = "aggregation"
        self.rucksack = rucksack
        self.file_name = self.rucksack.open['config']['file_name']
        if self.rucksack.open['config']['aggregation']['service']['name']:
            self.plugin_name = self.rucksack.open['config']['aggregation']['service']['name']

            # Getting computed data either from a webservice or local storage
            self.aggregator_location = self.rucksack.open['config']['aggregation']['service']['location']
            self.aggregator_service = {'local': 'local_cache', 'web': self.plugin_name}[self.aggregator_location]

    def run(self) -> object:
        # Getting corpus
        logger.debug(f"Getting corpus texts for {self.file_name}")
        self.rucksack.pack_corpus(SerialCorpus(self.rucksack).run())
        corpus_size = len(self.rucksack.open['data']['corpus'])

        # Getting gold
        logger.debug(f"Getting gold results for {self.file_name}")
        self.rucksack.pack_gold(GoldGS(self.rucksack).run())
        gold_size = len(self.rucksack.open['data']['gold'])

        # Getting computed
        if self.rucksack.open['config']['aggregation']['service']['name']:
            logger.debug(f"Getting computed results for {self.plugin_name} via {self.aggregator_location}")
            self.rucksack.pack_computed(self.run_plugin(self.pipeline_stage_name, self.aggregator_service,
                                                        self.rucksack))
            computed_size = len(self.rucksack.open['data']['computed'])
        else:
            logger.info(f"No aggregation plugin for computing defined")
            computed_size = 1

        if corpus_size <= 0 or gold_size <= 0 or computed_size <= 0:
            return False

        return self.rucksack


###############################################################################
class Evaluation(Pipeline):

    def __init__(self, rucksack):
        super(Evaluation, self).__init__()
        self.pipeline_stage_name = "evaluation"
        self.rucksack = rucksack
        self.evaluator_name = self.rucksack.open['config']["evaluation"]["name"]
        self.scorer_name = self.rucksack.open['config']["scoring"]['name']
        self.metrics_name = self.rucksack.open['config']["metrics"]['name']

    def run(self) -> object:
        self.rucksack.load_plugin('scoring', self.get_plugin('scoring', self.scorer_name))
        self.rucksack.load_plugin('metrics', self.get_plugin('metrics', self.metrics_name))
        self.rucksack = self.run_plugin(self.pipeline_stage_name, self.evaluator_name, self.rucksack)
        return self.rucksack


###############################################################################
class Storage(Pipeline):

    def __init__(self, rucksack):
        super(Storage, self).__init__()
        self.pipeline_stage_name = "storage"
        self.rucksack = rucksack
        self.config = self.rucksack.open['config']
        self.date = "{:%Y-%m-%d_%H:%M:%S.%f}".format(datetime.datetime.now())

    def run(self):
        if self.config.get('storage'):
            logger.debug(f"Storage Plugins: {self.config['storage']}")
            for item in self.config["storage"]:
                logger.debug(f"Running: {item}")
                self.run_plugin(self.pipeline_stage_name, item, self.rucksack)
        # print(dir(self.rucksack))
        print(self.rucksack.result_summary())
        return self.rucksack
