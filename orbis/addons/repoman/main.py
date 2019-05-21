import os

from . import corpora_downloader
from . import filter_downloader
from . import lense_downloader
from . import map_downloader


def download_everything():
    raise NotImplementedError


def menu():
    os.system('cls')  # on Windows
    os.system('clear')  # on linux / os x
    print("\nWelcome to Repoman!")
    print("What would you like to download?")
    print("[0]:\t Corpora")
    print("[1]:\t Filters")
    print("[2]:\t Lenses")
    print("[3]:\t Mappings")
    print("[4]:\t Everything")
    choice = int(input("-> "))
    if choice == 0:
        corpora_downloader.menu()
    elif choice == 1:
        filter_downloader.menu()
    elif choice == 2:
        lense_downloader.menu()
    elif choice == 3:
        map_downloader.menu()
    elif choice == 4:
        download_everything()
    else:
        menu()


def main():
    menu()


if __name__ == '__main__':
    main()
