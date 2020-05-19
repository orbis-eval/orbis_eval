# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path
from distutils.dir_util import copy_tree


def fill_config(user_dir, test_data_dir):
    # ToDo: check if data already filled!
    source = Path(test_data_dir) / '..' / 'orbis_config'
    # print(f"Data Dir: {source}")

    target = Path(user_dir) / "config"

    Path(target).mkdir(parents=True, exist_ok=True)

    print(f"Copying: {str(source)} -> {str(target)}")
    copy_tree(str(source), str(target))


def fill_data(user_dir, test_data_dir):
    # ToDo: check if data already filled!
    source = Path(test_data_dir) / 'corpora'
    # print(f"Data Dir: {source}")

    target = user_dir / "data" / "corpora"

    Path(target).mkdir(parents=True, exist_ok=True)

    print(f"Copying: {str(source)} -> {str(target)}")
    copy_tree(str(source), str(target))


def fill_queue(user_dir, test_data_dir):
    # ToDo: check if data already filled!
    source = Path(test_data_dir) / 'queue'
    # print(f"Queue Dir: {source}")

    target = user_dir / "queue" / "tests"
    target = os.path.abspath(str(target))

    Path(target).mkdir(parents=True, exist_ok=True)

    print(f"Copying: {str(source)} -> {str(target)}")
    copy_tree(str(source), str(target))


def create_orbis_external_folder(user_folder_settings_file, test_data_dir):
    default_dir = Path.home() / "orbis-eval"

    print("Where would you like to install the Orbis user directory?")
    user_dir = input(f"> ({str(default_dir)}):") or default_dir

    print(f"\nCreating: {user_dir}")
    Path(user_dir).mkdir(parents=True, exist_ok=True)

    with open(user_folder_settings_file, 'w', encoding='utf-8') as settings_file:
        settings_file.write(str(user_dir))

    fill_data(user_dir, test_data_dir)
    fill_queue(user_dir, test_data_dir)
    fill_config(user_dir, test_data_dir)
    # print("\n")
    return user_dir


def load_user_folder_path(user_folder_settings_file, test_data_dir):
    file = user_folder_settings_file

    # print(f"user_folder.txt ({file}) {os.path.isfile(file)}")

    if not os.path.isfile(file):
        print(f"User folder location not found. Creating new...\n")
        user_folder = create_orbis_external_folder(user_folder_settings_file, test_data_dir)

    with open(user_folder_settings_file, 'r', encoding='utf-8') as open_file:
        user_folder = open_file.read()

    if not os.path.isdir(user_folder):
        print(f"User folder location not found. Creating new...\n")
        user_folder = create_orbis_external_folder(user_folder_settings_file, test_data_dir)

    if not os.path.isfile(Path(user_folder) / 'config' / 'orbis_config'):
        # print(f"{user_folder_settings_file}")
        print(f"User settings location not found. Creating new...\n")
        fill_config(user_folder, test_data_dir)

    return user_folder


# /
source_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

# /orbis
package_root = os.path.join(source_root, 'orbis_eval')

#
test_data_dir = os.path.join(package_root, 'data', 'tests')

# ~/.orbis-eval.txt
user_folder_settings_file = os.path.join(Path.home() / '.orbis-eval.txt')

# e.g.: ~/orbis-eval
user_dir = load_user_folder_path(user_folder_settings_file, test_data_dir)

# /orbis/config/settings.json
settings_file = os.path.join(user_dir, 'config', 'settings.json')

# Load config as dict
with open(settings_file, 'r', encoding='utf-8') as open_file:
    config = json.load(open_file)

# ~/orbis-eval/data/corpora
corpora_dir = os.path.join(user_dir, 'data', 'corpora')

# ~/orbis-eval/logs
log_path = os.path.join(user_dir, 'logs')

# ~/orbis-eval/queue/activated
queue = os.path.join(user_dir, 'queue', 'activated')

# ~/orbis-eval/queue/tests
test_queue = os.path.join(user_dir, 'queue', 'tests')

# ~/orbis-eval/output
output_path = os.path.join(user_dir, 'output')
