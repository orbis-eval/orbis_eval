# -*- coding: utf-8 -*-

import datetime
import json
import os
import pathlib
import logging
logger = logging.getLogger(__name__)


def get_timestamp():
    return "{:%Y-%m-%d_%H:%M:%S}".format(datetime.datetime.now())


def create_folder(directory_name):
    pathlib.Path(directory_name).mkdir(parents=True, exist_ok=True)


def create_folders(paths, folders_to_create=None):
    default_folders_to_create = (
        paths.log_path,
        paths.output_path,
    )
    folders_to_create = folders_to_create or default_folders_to_create
    for path in folders_to_create:
        create_folder(path)


def check_folders(paths, folders_to_create=None):
    default_folders_to_check = (
        paths.log_path,
        paths.output_path,
    )
    folders_to_check = folders_to_create or default_folders_to_check
    folders_not_found = [path for path in folders_to_check if not pathlib.Path(path).is_dir()]
    if len(folders_not_found) > 0:
        unfound_folders = []
        for path in folders_not_found:
            # Can not log this error since logger is not yet loaded
            print(f"Folder not found: {path}. Please reinstall Orbis or fix manually!")
            unfound_folders.append(path)
        raise NotADirectoryError(str(unfound_folders))


def save_rucksack(file, path, rucksack):

    dir = os.path.join(path, file)

    with open(dir, "w", encoding="utf-8") as open_file:
        json.dump(rucksack.open, open_file, indent=4, skipkeys=True)


def build_file_name(config, base_path, module_name, ending, raw=False):
    """
    Under construction!
    """
    return NotImplementedError

    # eg: /output/html_pages/
    file_path = os.path.join(base_path, module_name)

    aggregator_name = config["aggregation"]["service"]["name"]
    aggregator_source = config["aggregation"]["service"]["location"]
    entities = "_{}_".format("_".join(config["scorer"]["entities"]))
    file_name, ending = file_name.split(".")
    run_name = config["file_name"].split(".")[0]
    source = f'{aggregator_name}_{aggregator_source}_'
    entities = "_{}_".format("_".join(config["scorer"]["entities"]))
    file_name = "{}_-_{}-{}-{}-{}.{}".format(run_name, file_name, source, entities, get_timestamp(), ending)
    file_name = os.path.join(paths.output_path, file_name)

    if raw:
        # /output/module_name
        file_name = os.path.join(output_path, module_name)

    elif file_name[-1] == "/":
        file_name = config["file_name"].split(".")[0]
        file_name = f"{file_name}_{get_timestamp()}"
        file_name = os.path.join(output_path, file_name)

    else:
        try:
            file_name, ending = file_name.split(".")
            run_name = config["file_name"].split(".")[0]
            source = f'{aggregator_name}_{aggregator_source}_'
            entities = "_{}_".format("_".join(config["scorer"]["entities"]))
            file_name = "{}_-_{}-{}-{}-{}.{}".format(run_name, file_name, source, entities, get_timestamp(), ending)
            file_name = os.path.join(paths.output_path, file_name)

        except ValueError:
            file_name = f'{file_name}_{"-".join(config["scorer"]["entities"])}'
            file_name = f"{file_name}_{get_timestamp()}"
            file_name = os.path.join(paths.output_path, file_name)

    return file_path



