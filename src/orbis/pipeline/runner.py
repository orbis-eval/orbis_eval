#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-



from orbis import app
from orbis.pipeline import aggregation
from orbis.pipeline import evaluation
from orbis.pipeline import savor
from orbis.libs import config_lib


class Runner(object):
    """ Controls the evaluation pipeline and manages the data during
    an evaluation run. This class gets initialized with the config
    yaml as input. The single evaluation steps are then run using the config.
    This class is used instead of a pipeline that would be loacted
    in __main__.py
    """

    def __init__(self, **kwargs):
        """ The config is loaded from the yaml file.
        """
        self.config = config_lib.load_yaml_config(kwargs["config_yaml"])
        self.data = None
        self.results = None

    def run(self):

        app.logger.info("Running: {}".format(self.config["file_name"]))

        app.logger.info("Starting Aggregating for {}".format(self.config["file_name"]))
        # a = aggregation.Aggregator.get_class(self.config)  # no class_method anymore?
        a = aggregation.Aggregator(self.config)
        self.data = a.run()

        # Evaluation Runner
        app.logger.info("Starting Evaluation for {}".format(self.config["file_name"]))
        e = evaluation.Evaluator.get_class(self.config)
        self.data, self.results = e.fetch(self.data)

        # Result Serializer
        # s = savor.Savor(self.config, self.data)
        # s.save()
        s = savor.Savor(self.config, self.data, self.results)
        s.run()
