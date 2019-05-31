from . import corpus
from . import monocle
from orbis.lib import addons

from . import addon_path


def menu():
    addons.clear_screen()

    print("\nWelcome to Repoman!")
    print("What would you like to download?")
    print("[0]:\t Corpora")
    print("[1]:\t Filters")
    print("[2]:\t Lenses")
    print("[3]:\t Mappings")
    print("[4]:\t Everything")
    choice = int(input("-> "))

    if choice == 0:
        corpus.main(addon_path).run()
    elif choice == 1:
        monocle.filter_downloader.menu()
    elif choice == 2:
        monocle.lense_downloader.menu()
    elif choice == 3:
        monocle.map_downloader.menu()
    elif choice == 4:
        print("Not implemented yet")
        menu()
    else:
        menu()


def main():
    menu()


if __name__ == '__main__':
    main()
