
import glob
import os
import requests

from orbis import app
from orbis.libs.entity_type_lib import normalize_entity_type
from orbis.libs.entity_type_lib import get_dbpedia_type
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
        app.logger.info("Requesting from Babelnet: {} ({})".format(file_dir.split("/")[-1], corpus_path.split("/data/")[-1].replace("/", "_")))

        file_name = file_dir.split("/")[-1]
        file_number = file_name.split(".")[0]

        cached_file = os.path.abspath(os.path.join(computed_path, file_number + ".json"))
        if os.path.isfile(cached_file):
            app.logger.info("Already received from Babelnet: {}".format(file_dir.split("/")[-1]))
            continue

        with open(file_dir) as open_file:
            text = open_file.read()
            response = query(text=text)

        response_json = response.json()
        file_entities = []

        for item in response_json:

            item["key"] = item["DBpediaURL"]

            item["entity_type"] = get_dbpedia_type(item["key"])
            item["entity_type"] = normalize_entity_type(item["entity_type"])

            item["key"] = apply_mapping(mapping, item["key"])

            item["document_start"] = int(item["charFragment"]["start"])
            item["document_end"] = int(item["charFragment"]["end"] + 1)

            item["surfaceForm"] = text[item["document_start"]:item["document_end"]]

            in_lense = apply_lense(lense, item["key"])
            to_filter = apply_filter(str_filter, item["surfaceForm"])

            if in_lense or not to_filter:
                file_entities.append(item)

        data[file_number]["computed"] = file_entities

        app.logger.info("Received from Babelnet: {}".format(file_dir.split("/")[-1]))

    return data


def query(text=None):
    service_url = 'https://babelfy.io/v1/disambiguate'
    key = os.environ['BABELNET_API_KEY']
    annotation_type = 'NAMED_ENTITIES'

    data = {
        'text': text,
        'annType': annotation_type,
        'key': key
    }

    response = requests.post(service_url, data=data)
    return response
