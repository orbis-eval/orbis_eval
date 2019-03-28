#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-



from orbis import app
from orbis.libs import evaluation_lib


class Evaluator(object):
    """docstring for Evaluator"""

    def __init__(self):
        self.config = None

        # Test if any configuration for Evaluator runner
        # if not self.config.get("evaluator", False):
        #     raise ValueError("No reader specified in yaml file.")

    @classmethod
    def get_class(cls, config):
        cls.config = config

        evaluator_class = eval(config["evaluator"]["name"])

        app.logger.info("Running {} for {}".format(cls.config["evaluator"]["name"], cls.config["file_name"]))

        return evaluator_class(config)

    def runn(self):
        kwargs = {
            "data": self.data,
            "config": self.config
        }
        app.logger.debug(self.config["evaluator"])
        for item in self.config["savor"]:
            app.logger.debug(item)
            kwargs["plugin_name"] = item
            evaluation_lib.get_evaluation(kwargs)


class NEL_Evaluator(Evaluator):
    """docstring for NEL_Evaluator"""

    def __init__(self, config):
        super(NEL_Evaluator, self).__init__()
        self.config = config

    def fetch(self, data):
        return self.evaluation(data, evaluation_lib.get_conditions(self.config))

    def evaluation(self, data, conditions):
        data, results = evaluation_lib.get_binary_classification(self.config, data, conditions)
        return data, results
