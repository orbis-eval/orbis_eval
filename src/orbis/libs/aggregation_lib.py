#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import glob
import json
import os
import importlib

from orbis import app
from orbis.libs import entity_type_lib
from orbis.libs.entity_preprocessing_lib import apply_lense
from orbis.libs.entity_preprocessing_lib import apply_filter
from orbis.libs.entity_preprocessing_lib import apply_mapping


def get_corpus(config_dict: dict, data: dict) -> dict:
    """Gets the corpus data from a directory

    :param data:
    :param config_dict:
    :return:
    """

    corpus_path = os.path.abspath(os.path.join(config_dict['corpus_path'], "*.txt"))

    for file_dir in glob.glob(corpus_path):
        file_number = file_dir.split("/")[-1].split(".")[0]

        with open(file_dir) as open_file:
            try:
                corpus = open_file.read()

            except Exception as exception:
                app.logger.error(f"Corpus file empty: {file_dir} ({exception})")
                corpus = ""

            data[file_number] = {
                "file_number": file_number,
                "corpus": corpus,
            }
            # app.logger.debug(f"get_corpus: {data[file_number]}")

    return data


def get_gold(config_dict: dict, data: dict) -> dict:
    """ Gets the corpus data from a directory

    :param config_dict:
    :param data:
    :return:
    """

    gold_dir = config_dict["gold_dir"]
    lense = config_dict["lense"]
    mapping = config_dict["mapping"]
    filter_ = config_dict["filter"]

    gold_path = os.path.abspath(os.path.join(gold_dir, "*.gs"))
    
    app.logger.debug(type(data))
    
    for file_number, item in data.items():
        if not item.get("gold"):
            item["gold"] = []

    for file_dir in glob.glob(gold_path):

        with open(file_dir) as open_file:

            for line in open_file.readlines():
                #  0    1    2   3    4    5
                # doc|start|end|url|score|type|

                nuggets = line.split()

                file_number = nuggets[0]
                start = int(nuggets[1])
                end = int(nuggets[2])
                score = nuggets[4]
                type_url = nuggets[5]
                url = nuggets[3].replace("%26", "&")  # Implement urllib method
                surface_form = data[file_number]["corpus"][start:end]

                app.logger.debug(f"Processing: {url}: {surface_form} ({type_url})")

                url = apply_mapping(mapping, url)
                in_lense = apply_lense(lense, url)
                to_filter = apply_filter(filter_, surface_form)

                entity_type = entity_type_lib.normalize_entity_type(type_url.split("/")[-1])

                if in_lense and not to_filter:
                    app.logger.debug(f"Adding {surface_form}")
                    data[file_number]["gold"].append({
                        "id": file_number,
                        "start": start,
                        "end": end,
                        "key": url,
                        "score": score,
                        "entity_type": entity_type,
                        "type_url": type_url,
                        "surfaceForm": surface_form
                    })
                else:
                    app.logger.debug(f"Not adding to gold: {surface_form}")
                app.logger.debug(f'get_gold: {data[file_number]["gold"]}')

    return data


def get_local(config_dict: dict, data: dict) -> dict:
    """

    :param data:
    :param config_dict:
    :return:
    """

    computed_path = config_dict["computed_path"]
    filter_ = config_dict["filter"]
    lense = config_dict["lense"]
    mapping = config_dict["mapping"]

    for file_dir in glob.glob(os.path.join(computed_path, "*.json")):
        file_number = file_dir.split("/")[-1].split(".")[0]
        data[file_number]["computed"] = []

        with open(file_dir) as open_file:
            for item in json.load(open_file):

                item["key"] = apply_mapping(mapping, item["key"])
                in_lense = apply_lense(lense, item["key"])
                to_filter = apply_filter(filter_, item["surfaceForm"])

                item["entity_type"] = entity_type_lib.normalize_entity_type(item["entity_type"])

                if item.get("entity_metadata"):
                    item["document_start"] = int(item["entity_metadata"]["document_index_start"][0])
                    item["document_end"] = int(item["entity_metadata"]["document_index_end"][0])

                if in_lense and not to_filter:
                    data[file_number]["computed"].append(item)

    # app.logger.debug(f"get_local: {data}")
    return data


def get_from_webservice(config_dict: dict, data: dict):
    """

    :param config_dict:
    :param data:
    :return:
    """

    try:
        plugin_name = config_dict["plugin_name"]

    except Exception:
        error = ValueError("plugin_name not found in config.")
        app.logger.critical(error)
        raise ValueError(error)

    app.logger.info(f"Running aggregator plugin: {plugin_name}")
    webservice = importlib.import_module(f"orbis.plugins.aggregators.{plugin_name}.{plugin_name}")

    data = webservice.run(config_dict, data)

    return data
