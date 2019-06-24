#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import time
import importlib

from . import config
from orbis.libs.decorators import clear_screen


# TODO: Needs to be implemented directly into the
# corpus folder as info-file or config-file


@clear_screen()
def start_menu():
    print("\nWelcome to Repoman!")
    print("What would you like to download?")
    for number, item in config.start_menu_options.items():
        print(f"[{number}]:\t {item}")


def select():
    choice = config.start_menu_options.get(input("-> "), None)

    if choice:
        module_path = f"orbis.addons.repoman.{choice.lower()}"
        imported_module = importlib.import_module(module_path)
        imported_module.Main().run()
    else:
        print("Not implemented yet")
        time.sleep(4)
        start_menu()


@clear_screen()
def run():
    start_menu()
    select()
