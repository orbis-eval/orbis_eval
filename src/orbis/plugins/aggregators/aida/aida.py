import glob
import os
import requests
import html
from urllib.parse import unquote_plus

from orbis import app
from orbis.libs.entity_type_lib import normalize_entity_type
from orbis.libs.entity_preprocessing_lib import apply_lense
from orbis.libs.entity_preprocessing_lib import apply_filter
from orbis.libs.entity_preprocessing_lib import apply_mapping



def run(config_dict: dict, data: dict) -> dict:

    computed_path = config_dict["computed_path"]
    corpus_path = config_dict["corpus_path"]
    lense = config_dict["lense"]
    mapping = config_dict["mapping"]
    str_filter = config_dict["str_filter"]

    files = glob.glob(os.path.join(corpus_path, "*.txt"))

    for file_dir in sorted(files, key=lambda name: int(name.split("/")[-1].split(".")[0])):
        app.logger.info("Requesting from Aida: {} ({})".format(file_dir.split("/")[-1], corpus_path.split("/data/")[-1].replace("/", "_")))

        file_name = file_dir.split("/")[-1]
        file_number = file_name.split(".")[0]

        cached_file = os.path.abspath(os.path.join(computed_path, file_number + ".json"))
        if os.path.isfile(cached_file):
            app.logger.info("Already received from Aida: {}".format(file_dir.split("/")[-1]))
            continue

        with open(file_dir) as open_file:
            response = query(text=open_file.read())

        try:
            response_json = response.json()
        except Exception as exception:
            app.logger.error("{}  ({})".format(exception, file_name))

        file_entities = []

        for idx, item in enumerate(response_json["mentions"]):

            if len(item["allEntities"]) <= 0:
                continue

            identifier = item["bestEntity"]["kbIdentifier"]
            item["key"] = response_json["entityMetadata"][identifier]["url"]

            item["key"] = html.unescape(item["key"])
            item["key"] = unquote_plus(item["key"])
            item["key"] = item["key"].replace("\n", "")
            item["key"] = item["key"].replace("http://en.wikipedia.org/wiki/", "http://dbpedia.org/resource/")
            item["key"] = item["key"].replace(" ", "_")

            types = response_json["entityMetadata"][identifier]["type"]

            item["key"] = apply_mapping(mapping, item["key"])

            if 'YAGO_wordnet_person_100007846' in types:
                item["entity_type"] = 'Person'
            elif 'YAGO_yagoGeoEntity' in types:
                item["entity_type"] = 'Place'
            elif 'YAGO_wordnet_organization_108008335' in types:
                item["entity_type"] = 'Organization'
            else:
                item["entity_type"] = 'NoType'

            item["entity_type"] = normalize_entity_type(item["entity_type"])

            item["document_start"] = int(item["offset"])
            item["document_end"] = int(item["document_start"] + int(item["length"]))
            item["surfaceForm"] = item["name"]

            in_lense = apply_lense(lense, item["key"])
            to_filter = apply_filter(str_filter, item["surfaceForm"])

            if in_lense or not to_filter:
                file_entities.append(item)

        data[file_number]["computed"] = file_entities

        app.logger.info("Received from Aida: {}".format(file_dir.split("/")[-1]))

    return data


def query(text=None):
    service_url = 'https://gate.d5.mpi-inf.mpg.de/aida/service/disambiguate'
    data = {'text': text}
    response = requests.post(service_url, data=data)
    return response
