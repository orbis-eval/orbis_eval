# -*- coding: utf-8 -*-

import datetime

from orbis_eval import app
from orbis_eval.core.rucksack import Rucksack
from orbis_eval.libs.files import save_rucksack
from orbis_eval.libs.plugins import load_plugin


class Pipeline(object):

    def __init__(self):
        super(Pipeline, self).__init__()

    def load(self, config):
        self.rucksack = Rucksack(config)
        self.file_name = self.rucksack.open['config']['file_name']

    def get_plugin(self, pipeline_stage_name, plugin_name):
        app.logger.debug(f"Getting {pipeline_stage_name} plugin: {plugin_name}")
        imported_module = load_plugin(pipeline_stage_name, plugin_name)
        module_class_object = imported_module.Main
        return module_class_object

    @classmethod
    def run_plugin(cls, pipeline_stage_name, plugin_name, rucksack):
        app.logger.debug(f"Running {pipeline_stage_name} plugin: {plugin_name}")
        plugin = cls.get_plugin(cls, pipeline_stage_name, plugin_name)
        rucksack = plugin(rucksack).run()
        return rucksack

    def run(self):
        app.logger.debug(f"Running: {self.file_name}")

        # Aggregation
        app.logger.debug(f"Starting aggregation for {self.file_name}")
        self.rucksack = Aggregation(self.rucksack).run()

        # Evaluation
        app.logger.debug(f"Starting evaluation for {self.file_name}")
        self.rucksack = Evaluation(self.rucksack).run()
        save_rucksack(f"{app.paths.log_path}/rucksack_{self.file_name}.json", app.paths.log_path, self.rucksack)

        # Storage
        app.logger.debug(f"Starting storage for {self.file_name}")
        self.rucksack = Storage(self.rucksack).run()

        return self.rucksack


###############################################################################
class Aggregation(Pipeline):

    def __init__(self, rucksack):
        super(Aggregation, self).__init__()
        self.pipeline_stage_name = "aggregation"
        self.rucksack = rucksack
        self.file_name = self.rucksack.open['config']['file_name']
        self.plugin_name = self.rucksack.open['config']['aggregation']['service']['name']

        # Getting computed data either from a webservice or local storage
        self.aggregator_location = self.rucksack.open['config']['aggregation']['service']['location']
        self.aggregator_service = {'local': 'local_cache', 'web': self.plugin_name}[self.aggregator_location]

    def run(self) -> object:
        # Getting corpus
        app.logger.debug(f"Getting corpus texts for {self.file_name}")
        self.rucksack.pack_corpus(self.run_plugin(self.pipeline_stage_name, "serial_corpus", self.rucksack))

        # Getting gold
        app.logger.debug(f"Getting gold results for {self.file_name}")
        self.rucksack.pack_gold(self.run_plugin(self.pipeline_stage_name, "gold_gs", self.rucksack))

        # Getting computed
        app.logger.debug(f"Getting computed results for {self.plugin_name} via {self.aggregator_location}")
        self.rucksack.pack_computed(self.run_plugin(self.pipeline_stage_name, self.aggregator_service, self.rucksack))
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
            for item in self.config["storage"]:
                app.logger.debug(f"Running: {item}")
                self.run_plugin(self.pipeline_stage_name, item, self.rucksack)
        return self.rucksack
