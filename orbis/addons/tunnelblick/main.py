#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import glob

from orbis import app

from .html_pages import HTMLPages


def get_folder_names():
    return [(corpus.strip("/").split("/")[-1], corpus) for corpus in glob.glob(os.path.join(app.paths.corpora_dir, "*/"))]


def menu():
    os.system('cls')  # on Windows
    os.system('clear')  # on linux / os x

    print("\nWelcome to Tunnelblick!")
    print("Which corpus would you like to look at?")

    corpora = get_folder_names()
    for idx, (corpus, corpus_path) in enumerate(corpora):
        print(f"[{idx}]:\t {corpus} ({corpus_path})")
    selection = int(input("--> "))

    hp = HTMLPages(*corpora[selection])
    hp.run()


def main():
    menu()


if __name__ == '__main__':
    main()
