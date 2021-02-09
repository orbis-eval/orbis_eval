import os

from .gs_handler import GsHandler
from .json_handler import JsonHandler


def get_gold_file_handler(rucksack, gold_path):
    if _check_has_file_type(gold_path, ".gs"):
        return GsHandler(rucksack, gold_path)
    elif _check_has_file_type(gold_path, ".json.gz"):
        return JsonHandler(rucksack, gold_path)
    else:
        raise TypeError(f"no valid gold document files found in {gold_path}")


def _check_has_file_type(directory, file_type):
    for file_name in os.listdir(directory):
        if file_name.endswith(file_type):
            return True
    return False
