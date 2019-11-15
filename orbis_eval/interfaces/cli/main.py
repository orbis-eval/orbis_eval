import os

from orbis_eval.libs.decorators import clear_screen

from .ascii import orbis_eval_logo


@clear_screen()
def start_menu():
    print(orbis_eval_logo)


@clear_screen()
def run():
    start_menu()
