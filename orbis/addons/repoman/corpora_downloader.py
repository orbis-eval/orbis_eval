from urllib.request import urlopen, urlretrieve
import re
import json
import os
import pathlib
from rdflib import Graph, Namespace
import shutil
# from SPARQLWrapper import SPARQLWrapper, JSON

from orbis.config import paths
from orbis.plugins.aggregation import dbpedia_entity_types


nif_namespace = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
itsrdf_namespace = Namespace("http://www.w3.org/2005/11/its/rdf#")
GERBIL_CORPORA = "https://github.com/dice-group/gerbil/tree/master/src/main/resources/dataId/corpora"


def extract_files_from_nif_corpus(g, folder):
    """
    Extracts the documents from a NIF corpus/corpora.
    :param turtle_input:
    :param folder: the ouput folder for the corpus
    :returns: -
    """
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    for subject, predicate, object_ in g.triples((None, nif_namespace.isString, None)):
        document_number = (subject.split("/")[-1]).split("#")[0]
        filename = os.path.join(folder, document_number + ".txt")
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as open_file:
                open_file.write(object_)


def extract_entities_from_nif_corpus(g, folder, file_name):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(folder, file_name), "w") as open_file:
        for subject, predicate, object_ in g.triples((None, nif_namespace.anchorOf, None)):
            subject_id = subject.split("/")[-1]
            document_number, postition = subject_id.split("#")
            start, end = postition.split("=")[-1].split(",")
            surfaceForm = object_
            subject_2 = subject
            for subject_2, predicate_2, object_2 in g.triples((subject, itsrdf_namespace.taIdentRef, None)):
                type_ = dbpedia_entity_types.get_dbpedia_type(object_2)
                line = "\t".join([document_number, start, end, object_2.strip(), "1", type_, surfaceForm])
                open_file.write(line + "\n")


def get_available_corpora():
    available_corpora = {}
    with urlopen(GERBIL_CORPORA) as gerbil_corpora:
        gerbil_html = gerbil_corpora.read().decode("utf-8")
    regex = r"href=\"(.*?dice-group.*?\.json)\""
    matches = re.finditer(regex, gerbil_html, re.MULTILINE)
    for match in matches:
        # print(f"https://github.com{match.group(1)}")
        corpus_name = match.group(1).split("/")[-1].split(".")[0]
        available_corpora[corpus_name] = f"{match.group(1)}"
    # print(available_corpora)
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


def save_ttl(download_destination, corpus_dir, download_name):
    g = Graph()
    g.parse(download_destination, format="turtle")
    extract_files_from_nif_corpus(g, os.path.join(corpus_dir, "corpus"))
    extract_entities_from_nif_corpus(g, os.path.join(corpus_dir, "gold"), f"{download_name}.gs")


def download_corpus(corpus_name, corpus_url):
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
        save_ttl(download_destination, corpus_dir, download_name)


def load_corpus():
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
        save_ttl(file_destination, corpus_dir, file_name)


def list_available_corpora():
    """
    Only supporting ttl's right now. Zipped or xml content will be ignored.
    """
    available_corpora = get_available_corpora()
    list_of_available_corpora = []
    for corpus_name, corpus_url in available_corpora.items():
        corpus_dict = get_corpus_dict(corpus_url)
        corpus_download = get_corpus_download(corpus_dict)
        # print(f"{corpus_name}: {corpus_download}")
        file_type = corpus_download.split(".")[-1]
        if file_type == "ttl":
            list_of_available_corpora.append((corpus_name, corpus_download))
    for idx, corpus in enumerate(list_of_available_corpora):
        print(f'[{idx}]:\t {corpus[0]}')
    print(f'[{idx + 1}]:\t Load local NIF corpus file')
    selection = int(input("Selection: "))
    if selection == idx + 1:
        load_corpus()
    else:
        download_corpus(*list_of_available_corpora[selection])


def menu(all=False):
    os.system('cls')  # on Windows
    os.system('clear')  # on linux / os x
    print("Please select the corpus you want to download:")
    list_available_corpora()
