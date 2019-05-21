#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
.. moduleauthor:: Fabian Odoni fabian.odoni@htwchur.ch

"""

import ast
import subprocess
import sys

from orbis import app
from orbis.plugins.aggregation import dbpedia_entity_types
from orbis.core.aggregation import AggregationBaseClass


class RecognizeAggregator(AggregationBaseClass):
    """docstring for RecognizeAggregator"""

    def query(self, text, item):

        profile_name = self.rucksack.open['config']['aggregation']['service'].get('profile', "DBPEDIA")
        doc_id = item['index']

        if not all([text, isinstance(text, str), profile_name, isinstance(profile_name, str)]):
            raise KeyError  # Not clear error...

        executable = sys.modules[__name__].__file__.replace(__file__.split("/")[-1], "weblyzard_recognize_api.py")

        command = ["python2.7", executable, "-t", text, "-p", profile_name]
        if doc_id:
            command.append("-i")
            command.append(doc_id)
        command.append("-r")

        app.logger.debug("[orbis api] Running external Python 2.7 Script: {}".format(command))

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()

        # multiline_logging(app, output)

        if len(err) > 0:
            app.logger.error("** {}".format(err))
            output = []
        else:
            output = str(output.decode("utf-8"))
            output = ast.literal_eval(output)

        return output

    def map_entities(self, response, item):
        file_entities = []
        for idx, item in enumerate(response["annotations"]):
            item["entity_type"] = dbpedia_entity_types.normalize_entity_type(item["entity_type"])
            item["document_start"] = int(item["start"])
            item["document_end"] = int(item["end"])
            file_entities.append(item)
        return file_entities
