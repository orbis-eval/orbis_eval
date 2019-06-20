#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""Summary
"""
import importlib
import datetime

from orbis import app
from orbis.core.rucksack import Rucksack
from orbis.libs.files import save_rucksack


class Pipeline(object):

    """Summary

    Attributes:
        file_name (TYPE): Description
        rucksack (TYPE): Description
    """

    def __init__(self):
        """Summary
        """
        super(Pipeline, self).__init__()

    def load(self, config):
        """Summary

        Args:
            config (TYPE): Description
        """
        self.rucksack = Rucksack(config)
        self.file_name = self.rucksack.open['config']['file_name']

    def get_plugin(self, pipeline_stage_name, plugin_name):
        """Summary

        Args:
            pipeline_stage_name (TYPE): Description
            plugin_name (TYPE): Description

        Returns:
            TYPE: Description
        """
        app.logger.debug(f"Getting {pipeline_stage_name} plugin: {plugin_name}")
        module_path = f"orbis.plugins.{pipeline_stage_name}.{plugin_name}"
        imported_module = importlib.import_module(module_path)
        module_class_object = imported_module.Module
        return module_class_object

    @classmethod
    def run_plugin(cls, pipeline_stage_name, plugin_name, rucksack):
        """Summary

        Args:
            pipeline_stage_name (TYPE): Description
            plugin_name (TYPE): Description
            rucksack (TYPE): Description

        Returns:
            TYPE: Description
        """
        app.logger.debug(f"Running {pipeline_stage_name} plugin: {plugin_name}")
        plugin = cls.get_plugin(cls, pipeline_stage_name, plugin_name)
        rucksack = plugin(rucksack).run()
        return rucksack

    def run(self):
        """Summary
        """
        app.logger.debug(f"Running: {self.file_name}")

        # Aggregation
        app.logger.debug(f"Starting aggregation for {self.file_name}")
        self.rucksack = Aggregation(self.rucksack).run()

        # Evaluation
        app.logger.debug(f"Starting evaluation for {self.file_name}")
        self.rucksack = Evaluation(self.rucksack).run()

        # app.logger.debug(self.rucksack.open)
        save_rucksack(f"rucksack_{self.file_name}.json", app.paths.log_path, self.rucksack)

        # """
        # Storage
        app.logger.debug(f"Starting storage for {self.file_name}")
        self.rucksack = Storage(self.rucksack).run()
        # """


###############################################################################
class Aggregation(Pipeline):
    """Summary

    Attributes:
        aggregator_location (TYPE): Description
        aggregator_service (TYPE): Description
        file_name (TYPE): Description
        pipeline_stage_name (str): Description
        plugin_name (TYPE): Description
        rucksack (TYPE): Description
    """

    def __init__(self, rucksack):
        """Summary

        Args:
            rucksack (TYPE): Description
        """
        super(Aggregation, self).__init__()
        self.pipeline_stage_name = "aggregation"
        self.rucksack = rucksack
        self.file_name = self.rucksack.open['config']['file_name']
        self.plugin_name = self.rucksack.open['config']['aggregation']['service']['name']

        # Getting computed data either form a webservice or local storage
        self.aggregator_location = self.rucksack.open['config']['aggregation']['service']['location']
        self.aggregator_service = {'local': 'local_cache', 'web': self.plugin_name}[self.aggregator_location]

    def run(self) -> object:
        """Summary

        Returns:
            object: Description
        """
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

    """Summary

    Attributes:
        evaluator_name (TYPE): Description
        metrics_name (TYPE): Description
        pipeline_stage_name (str): Description
        rucksack (TYPE): Description
        scorer_name (TYPE): Description
    """

    def __init__(self, rucksack):
        """Summary

        Args:
            rucksack (TYPE): Description
        """
        super(Evaluation, self).__init__()

        self.pipeline_stage_name = "evaluation"
        self.rucksack = rucksack

        self.evaluator_name = self.rucksack.open['config']["evaluation"]["name"]
        self.scorer_name = self.rucksack.open['config']["scoring"]['name']
        self.metrics_name = self.rucksack.open['config']["metrics"]['name']

    def run(self) -> object:
        """Summary

        Returns:
            object: Description
        """
        self.rucksack.load_plugin('scoring', self.get_plugin('scoring', self.scorer_name))
        self.rucksack.load_plugin('metrics', self.get_plugin('metrics', self.metrics_name))
        self.rucksack = self.run_plugin(self.pipeline_stage_name, self.evaluator_name, self.rucksack)
        return self.rucksack


###############################################################################
class Storage(Pipeline):

    """Summary

    Attributes:
        config (TYPE): Description
        date (TYPE): Description
        pipeline_stage_name (str): Description
        rucksack (TYPE): Description
    """

    def __init__(self, rucksack):
        """Summary

        Args:
            rucksack (TYPE): Description
        """
        super(Storage, self).__init__()
        self.pipeline_stage_name = "storage"
        self.rucksack = rucksack
        self.config = self.rucksack.open['config']
        self.date = "{:%Y-%m-%d_%H:%M:%S.%f}".format(datetime.datetime.now())

    def run(self):
        """Summary

        Returns:
            TYPE: Description
        """
        if self.config.get('storage'):
            for item in self.config["storage"]:
                app.logger.debug(f"Running: {item}")
                self.run_plugin(self.pipeline_stage_name, item, self.rucksack)
        return self.rucksack
