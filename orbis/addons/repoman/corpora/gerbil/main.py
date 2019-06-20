from urllib.request import urlopen, urlretrieve
import re
import json
import os
import pathlib
import shutil

from orbis.config import paths
from orbis.addons.repoman.format.nif import convert


def list_available_corpora(config):
    """
    Only supporting ttl's right now. Zipped or xml content will be ignored.
    """

    list_of_available_corpora = []
    for file_format in config['corpora']:
        for source in config['corpora'][file_format]:
            if source != "gerbil":
                continue

            if file_format == "nif":
                corpora = get_nif_corpora(config['corpora'][file_format][source])
                list_of_available_corpora += corpora

    return list_of_available_corpora


def get_nif_corpora(source_urls):

    available_corpora = get_gerbil_corpora_list(source_urls)
    list_of_available_corpora = []
    for corpus_name, corpus_url in available_corpora.items():
        corpus_dict = get_corpus_dict(corpus_url)
        corpus_download = get_corpus_download(corpus_dict)
        # print(f"{corpus_name}: {corpus_download}")
        file_type = corpus_download.split(".")[-1]

        if file_type == "ttl":
            list_of_available_corpora.append((corpus_name, corpus_download, "nif"))
        else:
            print(f"Corpus not supported yet: {corpus_name} ({corpus_download})")

    return list_of_available_corpora


def get_gerbil_corpora_list(source_urls):

    available_corpora = {}
    for source in source_urls:

        with urlopen(source) as gerbil_corpora:
            gerbil_html = gerbil_corpora.read().decode("utf-8")

        # regex = r"href=\"(/dice-group/gerbil/blob/master/src/main/resources/dataId/corpora/.*?\.json)\""
        regex = r"href=\"(.*?dice-group.*?\.json)\""
        matches = re.finditer(regex, gerbil_html, re.MULTILINE)

        for match in matches:
            corpus_name = match.group(1).split("/")[-1].split(".")[0]
            available_corpora[corpus_name] = f"{match.group(1)}"

    return available_corpora


def get_corpus_dict(corpus_url):
    with urlopen(f"https://raw.githubusercontent.com{corpus_url.replace('/blob', '')}") as corpus:
        corpus_dict = json.loads(corpus.read(), encoding="utf-8")
    return corpus_dict


def get_corpus_download(corpus_dict):
    for item in corpus_dict['@graph']:
        item_types = item.get('@type')
        item_types = [item_types] if not isinstance(item_types, list) else item_types
        for type_ in item_types:
            if type_ in ['dataid:Distribution', 'dcat:Distribution']:
                return item['accessURL']


def download(corpus_name, corpus_url):
    corpus_dir = os.path.join(paths.corpora_dir, corpus_name.lower())
    if pathlib.Path(corpus_dir).is_dir():
        print(f"Corpus might exist already. A folder with the same name has been found: {corpus_dir}")
        overwrite = input("Do you want to overwrite it? (Y/n) ")
        if overwrite not in ["Y", "y", ""]:
            print("Download canceled.")
            return False
    pathlib.Path(corpus_dir).mkdir(parents=True, exist_ok=True)
    download_name = corpus_url.split("/")[-1].split(".")[0]
    download_filetype = corpus_url.split("/")[-1].split(".")[-1]
    download_destination = os.path.join(corpus_dir, "source")
    pathlib.Path(download_destination).mkdir(parents=True, exist_ok=True)
    download_destination = os.path.join(download_destination, f"{download_name}.{download_filetype}")
    urlretrieve(corpus_url, download_destination)
    if download_filetype == "ttl":
        convert.convert(download_destination, corpus_dir, download_name)


def load():
    file_path = input("Please enter path to NIF corpus file: ")
    file_name = ".".join(file_path.split("/")[-1].split(".")[:-1])

    file_name_ok = input(f'Is the corpus called "{file_name}"? (Y/n) ')
    while file_name_ok not in ["Y", "y", ""]:
        file_name = input("Please enter corpus name: ")
        file_name_ok = input(f"Is the corpus name {file_name} ok? (Y/n) ")

    corpus_dir = os.path.join(paths.corpora_dir, file_name.lower())
    if pathlib.Path(corpus_dir).is_dir():
        print(f"Corpus might exist already. A folder with the same name has been found: {corpus_dir}")
        overwrite = input("Do you want to overwrite it? (Y/n) ")
        if overwrite not in ["Y", "y", ""]:
            print("Download canceled.")
            return False

    pathlib.Path(corpus_dir).mkdir(parents=True, exist_ok=True)
    file_filetype = file_path.split("/")[-1].split(".")[-1]

    file_destination = os.path.join(corpus_dir, "source")
    pathlib.Path(file_destination).mkdir(parents=True, exist_ok=True)
    file_destination = os.path.join(file_destination, f"{file_name}.{file_filetype}")

    shutil.copy(str(file_path), str(file_destination))
    if file_filetype == "ttl":
        convert.convert(file_destination, corpus_dir, file_name)


def menu(all=False):
    os.system('cls')  # on Windows
    os.system('clear')  # on linux / os x
    print("Please select the corpus you want to download:")
    list_available_corpora()
