# -*- coding: utf-8 -*-

import argparse
import sys

from orbis_eval.libs.decorators import clear_screen
from orbis_eval.libs.addons import list_installed_addons

import logging
logger = logging.getLogger(__name__)


def get_addons():
    """
    Fetches a list of all installed addons. An addon is installed, if it's located in its own
    folder in the orbis addon directory. Because of that, we can just scan the orbis addon
    directory, only select the folders and also remove any directories starting with a dunder ("__").
    """
    return sorted([(name, module) for name, module in list_installed_addons().items()])


def get_description(addon_name):
    """
    Fetches the description out of description.txt file that is located in the
    folder of the addon. If it doesn't exist, this function returns None.
    """
    addon = list_installed_addons()[addon_name]
    Addon = addon.Main()
    Addon.get_description()
    description = Addon.description
    return description


@clear_screen()
def addon_selection_menu(addon_list, msg=None):
    """
    Displays a menu of all the available addons
    """

    msg = msg or "Please select Addon to run."
    msg = msg + "\nEnter q to quit.\n"
    print(msg)

    for idx, addon in enumerate(addon_list):
        space = 5 - len(str(idx))
        description = get_description(addon[0])
        description_str = f"\n{(space + len(str(idx)) + 6) * ' '}{description}" if description else ""

        print(f"[{idx + 1}]:{space * ' '}{addon[0]}{description_str}\n")

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

    addon_name = addon_list[selected_addon - 1][0]
    confirmation = str(input(f"Do you want to run {addon_name.split('_')[-1].capitalize()} now? (Y/n)")).lower()
    if not (confirmation == "y" or confirmation == "j" or len(confirmation) == 0):
        addon_selection_menu(addon_list)

    return addon_name


def run():
    addon_list = get_addons()
    addon_name_list = [name for name, module in addon_list]
    addon_module_list = [module for name, module in addon_list]

    parser = argparse.ArgumentParser(description='Run a Orbis addon')
    parser.add_argument('addon', type=str, nargs='?', default=False)
    parser.add_argument('--logging', default="error", action='store', help='Set logging level')

    arg = parser.parse_args()

    if arg.logging:
        logger.debug("Setting logging level to {arg.logging}")
        logger.setLevel(arg.logging.upper())

    if arg.addon and arg.addon.lower() in [addon[0].split("orbis_addon_")[-1].lower() for addon in addon_list]:
        addon = addon_module_list[addon_name_list.index(f"orbis_addon_{arg.addon}")].Main()
        addon.run()
    elif len(addon_list) > 0:
        addon_name = addon_selection_menu(addon_list)
        # print(addon_list)
        addon = addon_module_list[addon_name_list.index(addon_name)].Main()
        addon.run()
    else:
        sys.exit("No addons installed.")


if __name__ == '__main__':
    run()
    # get_description("orbis_addon_repoman")
