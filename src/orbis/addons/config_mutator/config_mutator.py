#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import orbis
from orbis.config import paths

from orbis.addons.config_mutator import menu
from orbis.addons.config_mutator import recognize_profiles
from orbis.addons.config_mutator import templates

from glob import glob
import os


def header() -> None:
    """
    Clears the screen and prints the ascii turtle

    :return: True
    """

    os.system('cls')  # on Windows
    os.system('clear')  # on linux / os x
    print(templates.turtle)


def get_folder_names(corpora_dir: str) -> list:
    """

    :param corpora_dir: The directory pointing to the folder containing all the corpora.
        Standard would be: orbis/data/corpora
    :type corpora_dir: str
    :return: A list of corpora names

    :Example:

    >>> corpora_dir = ""
    >>> get_folder_names(corpora_dir)
    2
    """

    corpora = [corpus.strip("/").split("/")[-1] for corpus in glob(os.path.join(corpora_dir, "*/"))]

    return corpora


def get_aggregators(aggregator_dir: str = os.path.join(orbis.app.paths.plugins_path, "aggregators")) -> list:
    """

    :param aggregator_dir:
    :type aggregator_dir: str
    :return: A list of all directories in the aggregator directory in the plugin path
        (specified in the settings.paths).
    :rtype: list
    """

    aggregator_list = os.listdir(aggregator_dir)
    return aggregator_list


def list_resources(resources_path: str = paths.data_dir, resources=None) -> dict:
    """

    :param resources_path:
    :type resources_path: str
    :param resources:
    :return: A dict containing all the resources
    :rtype: dict
    """

    if resources is None:
        resources = ["lenses", "filters", "mappings"]

    resources_dict = {}
    for resource in resources:
        resources_dict[resource] = sorted(list(set([
            items.replace("." + items.split(".")[-1], "").split("/")[-1]
            for items in glob(os.path.join(resources_path, resource + "/*"))
        ])))
    return resources_dict


def get_settings() -> dict:
    """

    :return: The settings as a dict.
    :rtype: dict

    """

    settings = {}
    resources = list_resources()

    lenses = resources["lenses"]
    filters = resources["filters"]
    mappings = resources["mappings"]
    aggregation_sources = ["web", "local"]
    aggregators = get_aggregators()
    corpora = get_folder_names(paths.corpora_dir)
    output_folders = get_folder_names(paths.evaluation_configs_dir.rstrip("/activated"))

    settings["corpora"] = menu.run(corpora, "corpora", single_select=False, empty_select=False, msg=None)

    settings["aggregators"] = menu.run(aggregators, "aggregators", single_select=False, empty_select=False, msg=None)

    if settings["aggregators"] == "recognize":
        settings["profiles"] = menu.run(recognize_profiles.profiles, "profiles", single_select=False, empty_select=False, msg=None)
    else:
        settings["profiles"] = None

    settings["aggregation_source"] = menu.run(aggregation_sources, "aggregation source", single_select=True, empty_select=False, msg=None)

    settings["lenses"] = menu.run(lenses, "lenses", single_select=False, empty_select=True, msg=None)

    settings["filters"] = menu.run(filters, "filters", single_select=False, empty_select=True, msg=None)

    settings["mappings"] = menu.run(mappings, "mappings", single_select=False, empty_select=True, msg=None)

    settings["output_folder"] = menu.run(output_folders, "output_folder", single_select=True, empty_select=False, msg=None)

    return settings


def build_yamls(settings) -> None:
    """
    :param settings:
    """

    output_folder = settings["output_folder"][0]
    aggregation_source = settings["aggregation_source"][0]
    profiles = settings["profiles"]

    lenses = settings["lenses"]
    filters = settings["filters"]
    mappings = settings["mappings"]

    corpora = settings["corpora"]
    aggregators = settings["aggregators"]

    for corpus in corpora:

        for aggregator in aggregators:

            base_path = orbis.app.paths.evaluation_configs_dir.replace("/activated", "")
            with open(f"{base_path}/{output_folder}/{corpus}_{aggregator}_{aggregation_source}.yaml", "w") as open_file:

                if lenses:
                    lenses_str = ""
                    for lense in lenses:
                        lenses_str += f"     - {lense}\n"

                if mappings:
                    mappings_str = ""
                    for mapping in mappings:
                        mappings_str += f"     - {mapping}\n"

                if filters:
                    filters_str = ""
                    for filter_ in filters:
                        filters_str += f"     - {filter_}\n"

                content = {
                    "corpus": corpus,
                    "aggregator": aggregator,
                    "profile": f"\n    profile: {profiles}" if aggregator == "recognize" else "",
                    "location": aggregation_source,
                    "lenses": f"    lenses:\n{lenses_str}" if lenses else "",
                    "mappings": f"    mappings:\n{mappings_str}" if mappings else "",
                    "filters": f"    filters:\n{filters_str}" if filters else "",
                }

                yaml_content = templates.yaml_template.format(**content)
                open_file.write(yaml_content)


def main() -> None:
    """

    """

    settings = get_settings()
    profiles = settings["profiles"]

    if profiles is not None:
        for _ in profiles:
            build_yamls(settings)
    else:
        build_yamls(settings)

    header()
    print(" Config yamls generated. Good bye!")


if __name__ == '__main__':
    main()
