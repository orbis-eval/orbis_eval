#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import argparse
import os
import importlib
import sys

from orbis.config import paths
from orbis.libs.decorators import clear_screen


def get_addons():
    """
    Fetches a list of all installed addons. An addon is installed, if it's located in its own
    folder in the orbis addon directory. Because of that, we can just scan the orbis addon
    directory, only select the folders and also remove any directories starting with a dunder ("__").
    """
    return sorted([f.name for f in os.scandir(paths.addons_path) if f.is_dir() and not f.name.startswith("__")])


def get_description(addon_name):
    """
    Fetches the description out of description.txt file that is located in the
    folder of the addon. If it doesn't exist, this function returns None.
    """
    description_txt = f"{paths.addons_path}/{addon_name}/description.txt"
    try:
        with open(description_txt, "r", encoding="utf-8") as open_file:
            description = open_file.read().strip()
    except Exception:
        description = None

    return description


@clear_screen()
def addon_selection_menu(addon_list, msg=None):
    """
    Displays a menu of all the available addons
    """

    msg = msg or "Please select Addon to run."
    msg = msg + "\nEnter q to quit.\n"
    print(msg)

    for idx, addon_name in enumerate(addon_list):
        space = 5 - len(str(idx))
        description = get_description(addon_name)
        description_str = f"\n{(space + len(str(idx)) + 6) * ' '}{description}" if description else ""

        print(f"[{idx + 1}]:{space * ' '}{addon_name}{description_str}\n")

    selected_addon = input("\nPlease enter number of the addon you want to run: ")

    if selected_addon == "q":
        sys.exit("\nExiting Orbis addon menu. Bye\n")

    try:
        selected_addon = int(selected_addon)
    except Exception as exception:
        print(exception)
        addon_selection_menu(addon_list, f"\nInvalid input: {selected_addon}\nPlease try again.")

    if selected_addon not in range(1, len(addon_list) + 1):
        addon_selection_menu(addon_list, f"\nInvalid input: {selected_addon}\nPlease try again.")

    confirmation = str(input(f"Do you want to run {addon_list[selected_addon - 1]} now? (Y/n)")).lower()
    if not (confirmation == "y" or confirmation == "j" or len(confirmation) == 0):
        addon_selection_menu(addon_list)

    addon_name = addon_list[selected_addon - 1]

    return addon_name


def run():
    addon_list = get_addons()

    parser = argparse.ArgumentParser(description='Run a Orbis addon')
    parser.add_argument('addon', type=str, nargs='?', default=False)
    arg = parser.parse_args()

    if arg and arg.addon in addon_list:
        addon = importlib.import_module(f"orbis.addons.{arg.addon}.main")
        addon.run()
    elif len(addon_list) > 0:
        addon_name = addon_selection_menu(addon_list)
        addon = importlib.import_module(f"orbis.addons.{addon_name}.main")
        addon.run()
    else:
        sys.exit("No addons installed.")


if __name__ == '__main__':
    run()
