# -*- coding: utf-8 -*-

import json
import os
import pickle
import lzma
import html
from urllib.parse import unquote_plus

from orbis_eval.core import app
from orbis_eval.libs import cli

import logging
logger = logging.getLogger(__name__)


class Main(object):
    """docstring for Main"""

    def __init__(self):
        super(Main, self).__init__()

    @classmethod
    def run_monocle(cls, entities, data):
        result = []

        for item in entities:

            in_lense = True
            to_filter = False

            if data.get("mapping"):
                item["key"] = cls.apply_mapping(data["mapping"], item["key"])

            if data.get("lense"):
                in_lense = cls.apply_lense(data["lense"], item["key"])

            if data.get("str_filter"):
                to_filter = cls.apply_filter(data["str_filter"], item["surfaceForm"])

            if in_lense or not to_filter:
                result.append(item)

        return result

    @classmethod
    def build_source_path(cls, file_name: str, resource_type: str) -> str:
        file_path = os.path.abspath(os.path.join(os.path.join(app.paths.user_dir, f"{resource_type}s")))
        source_file = os.path.join(file_path, file_name + ".xz")
        return source_file

    @classmethod
    @cli.print_loading("lense", with_runtime=True)
    def load_lense(cls, file_names: list = False, refresh: bool = False) -> dict:
        file_path = os.path.abspath(os.path.join(os.path.join(app.paths.user_dir, f"{'lense'}s")))
        lense_dict = {}
        for file_name in file_names:
            pickle_file = os.path.join(file_path, file_name + ".pickle")
            source_file = os.path.join(file_path, file_name + ".xz")
            already_converted = os.path.isfile(pickle_file)
            source_available = os.path.isfile(source_file)
            if refresh or not already_converted:
                if not source_available:
                    raise RuntimeError(f"No Source to convert found {source_file}")
                logger.info("Converting lense to pickle")
                cls.convert_lense(source_file)
            with open(pickle_file, "rb") as pickle_file:
                new_lense_dict = pickle.load(pickle_file)
            lense_dict.update(new_lense_dict)
        return lense_dict

    @classmethod
    @cli.print_loading("mapping", with_runtime=True)
    def load_mapping(cls, file_names=False, refresh=False) -> dict:
        file_path = os.path.abspath(os.path.join(os.path.join(app.paths.user_dir, f"{'mapping'}s")))
        mapping_dict = {}
        for file_name in file_names:
            pickle_file = os.path.join(file_path, file_name + ".pickle")
            source_file = os.path.join(file_path, file_name + ".xz")
            already_converted = os.path.isfile(pickle_file)
            source_available = os.path.isfile(source_file)
            if refresh or not already_converted:
                if not source_available:
                    raise RuntimeError(f"No Source to convert found {source_file}")
                logger.info("Converting Mapping to pickle")
                cls.convert_mapping(source_file)
            with open(pickle_file, "rb") as pickle_file:
                new_mapping_dict = pickle.load(pickle_file)
            mapping_dict.update(new_mapping_dict)
        return mapping_dict

    @classmethod
    @cli.print_loading("filter", with_runtime=True)
    def load_filter(cls, file_names=False, refresh=False) -> dict:
        file_path = os.path.abspath(os.path.join(os.path.join(app.paths.user_dir, f"{'filter'}s")))
        filter_dict = {}
        for file_name in file_names:
            pickle_file = os.path.join(file_path, file_name + ".pickle")
            source_file = os.path.join(file_path, file_name + ".xz")
            already_converted = os.path.isfile(pickle_file)
            source_available = os.path.isfile(source_file)
            if refresh or not already_converted:
                if not source_available:
                    raise RuntimeError(f"No Source to convert found {source_file}")
                logger.info("Converting filter to pickle")
                cls.convert_filter(source_file)
            with open(pickle_file, "rb") as pickle_file:
                new_filter_dict = pickle.load(pickle_file)
            filter_dict.update(new_filter_dict)
        return filter_dict

    @classmethod
    def convert_resources(cls, source_dir: str, resource: str) -> None:
        if resource == "mapping":
            cls.convert_mapping(source_dir)
        if resource == "lense":
            cls.convert_lense(source_dir)
        if resource == "filter":
            cls.convert_filter(source_dir)

    @classmethod
    def convert_mapping(cls, source_dir: str) -> None:
        entity_map = {}
        with lzma.open(source_dir, "r") as open_file:
            redirects = json.load(open_file)
            redirects_len = len(redirects)
            dict_position = 0
            for source, redirects in redirects.items():
                source = source.replace(" ", "_")
                dict_position += 1
                for redirect in redirects:
                    cli.print_progress_bar(dict_position + 1, redirects_len, prefix='Progress:', suffix='Complete', length=50)
                    redirect = redirect.replace(" ", "_")
                    entity_map["http://dbpedia.org/resource/" + redirect] = "http://dbpedia.org/resource/" + source
                # entity_map[source] = source
        with open(source_dir.rstrip(".xz") + ".pickle", "wb") as open_file:
            pickle.dump(entity_map, open_file, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def convert_lense(cls, source_dir: str) -> None:
        entity_list_dict = {}
        with lzma.open(source_dir, "r") as open_file:
            entities = open_file.readlines()
            entity_len = len(entities)
            for idx, entity in enumerate(entities):
                cli.print_progress_bar(idx + 1, entity_len, prefix='Progress:', suffix='Complete', length=50)
                entity = entity.decode("utf8")
                entity = html.unescape(entity)
                entity = unquote_plus(entity)
                entity = entity.replace("\n", "")
                entity = entity.replace("http://en.wikipedia.org/wiki/", "http://dbpedia.org/resource/")
                entity = entity.replace(" ", "_")
                entity_list_dict[str(entity)] = True
        with open(source_dir.rstrip(".xz") + ".pickle", "wb") as open_file:
            pickle.dump(entity_list_dict, open_file, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def convert_filter(cls, source_dir: str) -> None:
        entity_list_dict = {}
        with lzma.open(source_dir, "r") as open_file:
            entities = open_file.readlines()
            entity_len = len(entities)
            for idx, entity in enumerate(entities):
                cli.print_progress_bar(idx + 1, entity_len, prefix='Progress:', suffix='Complete', length=50)
                print(entity)
                entity = str(entity).replace("\n", "")
                entity_list_dict[str(entity)] = True
        with open(source_dir.rstrip(".xz") + ".pickle", "wb") as open_file:
            pickle.dump(entity_list_dict, open_file, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def check_resources(cls, configs, refresh=False):
        logger.info("Checking for resources")
        resource_file_names = {"lenses": [], "mappings": [], "filters": []}

        for config in configs:
            logger.debug("Loading config file: {}".format(config.get("file_name", None)))
            for resource_type in ["lenses", "mappings", "filters"]:
                logger.debug("Working on: {}".format(resource_type))
                pickel_file_ending = ".pickle"
                # source_file_ending = ".txt" if resource_type == "filters" else ".xz"
                source_file_ending = ".xz"
                if config["aggregation"]["input"].get(resource_type):
                    file_path = os.path.abspath(os.path.join(os.path.join(app.paths.user_dir, "{}".format(resource_type))))
                    for file_name in config["aggregation"]["input"][resource_type]:
                        pickle_file = os.path.abspath(os.path.join(file_path, file_name + pickel_file_ending))
                        source_file = os.path.abspath(os.path.join(file_path, file_name + source_file_ending))
                        already_converted = os.path.isfile(pickle_file)
                        source_available = os.path.isfile(source_file)
                        if refresh or not already_converted:
                            if refresh:
                                logger.debug("Reconverting {} because of refresh request".format(resource_type))
                            if not already_converted:
                                logger.debug("Reconverting {} because pickle not found: {}".format(resource_type, pickle_file))
                            if not source_available:
                                # msg = "No Source to convert found: {}".format(config["aggregation"]["input"].get(resource_type))
                                msg = "No Source to convert found: {}".format(source_file)
                                raise RuntimeError(msg)
                            logger.debug("Converting {} to pickle: {}".format(resource_type, source_file))
                            cls.convert_resources(source_file, resource_type)
                        else:
                            logger.debug("Pickle for {} found".format(resource_type))
                    resource_file_names[resource_type].append(file_name)
                else:
                    logger.debug("No {} resources needed: {}".format(resource_type, config.get("file_name", None)))
        if len(resource_file_names["lenses"]) >= 0:
            file_names = resource_file_names["lenses"]
            app.lenses = cls.load_lense(file_names=file_names)
        else:
            logger.debug("No lenses needed for {}".format(config.get("file_name", None)))

        if len(resource_file_names["mappings"]) >= 0:
            file_names = resource_file_names["mappings"]
            app.mappings = cls.load_mapping(file_names=file_names)
        else:
            logger.debug("No mappings needed for {}".format(config.get("file_name", None)))

        if len(resource_file_names["filters"]) >= 0:
            file_names = resource_file_names["filters"]
            app.filters = cls.load_filter(file_names=file_names)
        else:
            logger.debug("No filters needed for {}".format(config.get("file_name", None)))

    @classmethod
    def apply_lense(cls, lense: dict, key: str) -> bool:
        in_lense = True
        if lense and key not in lense:
            logger.debug(f"Not in lense: {key}")
            in_lense = False
        return in_lense

    @classmethod
    def apply_filter(cls, str_filter: dict, surface_form: str) -> bool:
        in_filter = False
        if str_filter and surface_form in str_filter:
            logger.debug("{} will be filtered".format(surface_form))
            in_filter = True
        return in_filter

    @classmethod
    def apply_mapping(cls, mapping: dict, key: str) -> str:
        if mapping and mapping.get(key):
            logger.debug(f"{key} remapped to {mapping[key]}")
            key = mapping[key]
        return key
