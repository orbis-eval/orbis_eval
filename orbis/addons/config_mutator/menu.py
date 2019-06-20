#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from . import config_mutator


def init_msg(msg: str, item_name: str, single_select: bool) -> None:
    """

    :param msg:
    :param item_name:
    :param single_select:
    :return:
    """

    item_name = item_name.rstrip("s")
    if not msg:
        single_msg = " one " if single_select else " "
        item_name = item_name if single_select else item_name + "s"
        msg = f"\n Please select{single_msg}{item_name} to be used:\n"

    print(msg)


def add_none_selection(items: list, empty_select: bool) -> list:
    """

    :param items:
    :param empty_select:
    :return:
    """

    if empty_select:
        if None not in items:
            items = [None] + items

    return items


def list_selection(items: list) -> None:
    """

    :param items:
    :return:
    """
    for idx, item in enumerate(items):
        space = 5 - len(str(idx))
        print(f"  [{idx}]{space * ' '}{item}")


def get_selection(items: list, single_select: bool) -> list:
    """
    :param items:
    :param single_select:
    :return:
    """

    if single_select:
        response = input("\n Enter number of selection:")
    else:
        response = input("\n Enter numbers of selection separated by space (e.g. 23 42):")

    selection = [int(item) for item in response.split(" ")]

    if (single_select and len(selection) > 1) or (max(selection) > len(items)):
        return get_selection(items, single_select)

    selected_items = [items[int(item)] for item in selection]
    selected_items = selected_items if None not in selected_items else None

    print("\n You selected:")

    if selected_items:
        for selected_item in selected_items:
            print(f"  - {selected_item}")

    else:
        print("  - None")

    response = str(input("\n Is this correct? (Y/n)")).lower()

    if response == "y" or response == "j" or len(response) == 0:
        return selected_items

    else:
        return get_selection(items, single_select)


def run(items: list, item_name: str, single_select: bool = False, empty_select: bool = True, msg: str = None) -> list:
    """

    :param items:
    :param item_name:
    :param single_select:
    :param empty_select:
    :param msg:
    :return:
    """

    config_mutator.header()
    init_msg(msg, item_name, single_select)
    items = add_none_selection(items, empty_select)
    list_selection(items)
    selection = get_selection(items, single_select)

    return selection
