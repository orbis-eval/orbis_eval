import os
import importlib

from orbis.config import paths


def get_addons() -> list:
    addon_path = paths.addons_path
    addon_list = os.listdir(addon_path)
    return sorted(addon_list)


def addon_selection(addon_list: list) -> object:
    print("Please select Addon to run:\n")
    for idx, addon_name in enumerate(addon_list):
        space = 5 - len(str(idx))
        print(f"[{idx}]{space * ' '}{addon_name}")
    selected_addon = int(input("\nPlease enter number of the addon you want to run: "))
    confirmation = str(input(f"Do you want to run {addon_list[selected_addon]} now? (Y/n)")).lower()
    if not (confirmation == "y" or confirmation == "j" or len(confirmation) == 0):
        addon_selection(addon_list)
    addon_name = addon_list[selected_addon]
    addon = importlib.import_module(f"orbis.addons.{addon_name}.main")
    return addon


def clear_screen():
    os.system('cls')  # on Windows
    os.system('clear')  # on linux / os x


if __name__ == '__main__':
    addon_list = get_addons()
    print(addon_list)
    addon = addon_selection(addon_list)
    print(type(addon))
