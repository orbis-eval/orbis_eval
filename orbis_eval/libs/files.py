# -*- coding: utf-8 -*-

import datetime
import json
import os
import pathlib
import logging
import uuid

from mdutils.mdutils import MdUtils
from orbis_eval.__version__ import __version__ as orbis_version

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


def save_rucksack(path, rucksack, timestamp):
    result_uuid = uuid.uuid4().hex
    dir_rooksack = os.path.join(path, f"{result_uuid}-rooksack.json")
    os.makedirs(path)

    with open(dir_rooksack, "w", encoding="utf-8") as open_file:
        json.dump(rucksack.open, open_file, indent=4, skipkeys=True)

    create_md_result_file(path, rucksack, timestamp, result_uuid)


def create_md_result_file(path, rucksack, timestamp, result_uuid):
    dir_result = os.path.join(path, f"{result_uuid}-result.md")
    md_file = MdUtils(file_name=dir_result, title='Orbis Experiment')
    md_file.new_line("Your Experiments are completed")
    md_file.new_line("Metadata link: " + md_file.new_inline_link(link=f"{result_uuid}-rooksack.json"))
    md_file.new_line()
    result = rucksack.result_summary()
    if "binary_classification" in result:
        values = result["binary_classification"]
        result_rows = ["Annotator", "Dataset", "Micro F1 score", "Micro Precision", "Micro Recall", "Macro F1 score",
                       "Macro Precision", "Macro Recall", "Total True Positive", "Total False Positive",
                       "Total False Negative", "Total Items", "Entities", "Timestamp", "Orbis Version"]
        result_rows.extend([rucksack.config['aggregation']['service']['name'] if
                            'aggregation' in rucksack.config else 'None',
                            rucksack.config['aggregation']['input']['data_set']['name'] if
                            'aggregation' in rucksack.config else 'None',
                            f"{values['micro']['f1_score']:.4f}",
                            f"{values['micro']['recall']:.4f}",
                            f"{values['micro']['precision']:.4f}",
                            f"{values['macro']['f1_score']:.4f}",
                            f"{values['macro']['recall']:.4f}",
                            f"{values['macro']['precision']:.4f}",
                            f"{values['total_tp']:.4f}",
                            f"{values['total_fp']:.4f}",
                            f"{values['total_fn']:.4f}",
                            f"{values['total_item_sum']:.4f}",
                            " ".join(values['entities']),
                            timestamp, orbis_version
                            ])
        md_file.new_table(columns=15, rows=2, text=result_rows, text_align='center')
    else:
        md_file.new_line("No results!!!")

    md_file.create_md_file()


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
