import importlib
import pathlib
import os
import shutil
from urllib.request import urlopen, urlretrieve

from orbis.lib.config import load_config
from orbis.config import paths
from orbis.lib import addons


class Corpus(object):
    """docstring for Corpus"""

    def __init__(self, addon_path):
        super(Corpus, self).__init__()
        self.config = load_config([f"{addon_path}config.yaml"])[0]
        self.available_corpora = {}
        self.choice = {}
        self.selection = None

    def fetch_available(self):
        for file_format in self.config['corpora']:
            for source in self.config['corpora'][file_format]:
                module_path = f"orbis.addons.repoman.corpus.{source}.main"
                imported_module = importlib.import_module(module_path)
                corpora = imported_module.list_available_corpora(self.config)
                self.available_corpora[source] = corpora

    def select(self):

        addons.clear_screen()
        print("Please select the corpus you want to download:")

        counter = 0
        for source, item in self.available_corpora.items():
            source_hash = len(source) * "#"
            print(f"\n{source}\n{source_hash}")

            for corpus in self.available_corpora[source]:
                print(f'[{counter}]:\t {corpus[0]} ({corpus[2]})')
                self.choice[counter] = *corpus, source
                # self.choice[counter] = name, url, type, source
                # print(self.choice[counter])
                counter += 1

        print(f'[{counter}]:\t Load local corpus file')
        self.choice[counter] = ("local", None, None, "local")
        self.selection = int(input("Selection: "))

    def down_and_load(self):

        print(self.choice)
        action = "load" if self.choice[self.selection][0] == "local" else "download"

        if action == "local":
            source_available = self.load()
        else:
            source_available = self.download()

        if source_available:
            module_path = f"orbis.addons.repoman.format.{self.choice[self.selection][2]}.{action}"
            print(f">>>>>>> {module_path}")
            imported_module = importlib.import_module(module_path)
            imported_module.run(*self.choice[self.selection])

    def source_exists(self, corpus_dir):
        if pathlib.Path(corpus_dir).is_dir():
            print(f"Corpus might exist already. A folder with the same name has been found: {corpus_dir}")
            overwrite = input("Do you want to overwrite it? (Y/n) ")
            if overwrite not in ["Y", "y", ""]:
                print("Download canceled.")
                return True
        return False

    def download(self):

        corpus_url = self.choice[self.selection][1]
        download_name = corpus_url.split("/")[-1].split(".")[0]
        corpus_dir = os.path.join(paths.corpora_dir, download_name.lower())

        if not self.source_exists(corpus_dir):
            pathlib.Path(corpus_dir).mkdir(parents=True, exist_ok=True)
            download_name = corpus_url.split("/")[-1].split(".")[0]
            download_filetype = corpus_url.split("/")[-1].split(".")[-1]
            download_destination = os.path.join(corpus_dir, "source")
            pathlib.Path(download_destination).mkdir(parents=True, exist_ok=True)
            download_destination = os.path.join(download_destination, f"{download_name}.{download_filetype}")
            urlretrieve(corpus_url, download_destination)

            return download_destination
        return False

    def ask_for_format(self):
        module_path = f"orbis.addons.repoman.format"
        format_list = os.listdir(module_path)
        print("What's the format of the corpus?")

        for idx, format_name in enumerate(format_list):
            space = 5 - len(str(idx))
            print(f"[{idx}]{space * ' '}{format_name}")

        selected_format = int(input("\nPlease enter number of the addon you want to run: "))
        """
        confirmation = str(input(f"Do you want to run {addon_list[selected_format]} now? (Y/n)")).lower()
        if not (confirmation == "y" or confirmation == "j" or len(confirmation) == 0):
            addon_selection(addon_list)
        """
        format_name = format_list[selected_format]
        print(f">>>>>>> {format_name}")
        addon = importlib.import_module(f"orbis.addons.{format_name}.main")

    def load(self):
        file_path = input("Please enter path to corpus file: ")
        file_name = ".".join(file_path.split("/")[-1].split(".")[:-1])

        file_name_ok = input(f'Is the corpus called "{file_name}"? (Y/n) ')
        while file_name_ok not in ["Y", "y", ""]:
            file_name = input("Please enter corpus name: ")
            file_name_ok = input(f"Is the corpus name {file_name} ok? (Y/n) ")

        corpus_dir = os.path.join(paths.corpora_dir, file_name.lower())
        if not self.source_exists(corpus_dir):

            pathlib.Path(corpus_dir).mkdir(parents=True, exist_ok=True)
            file_filetype = file_path.split("/")[-1].split(".")[-1]

            file_destination = os.path.join(corpus_dir, "source")
            pathlib.Path(file_destination).mkdir(parents=True, exist_ok=True)
            file_destination = os.path.join(file_destination, f"{file_name}.{file_filetype}")
            shutil.copy(str(file_path), str(file_destination))

            return file_destination
        return False

    def run(self):
        self.fetch_available()
        self.select()
        self.down_and_load()
