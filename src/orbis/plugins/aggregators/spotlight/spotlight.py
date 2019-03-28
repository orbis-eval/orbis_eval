from orbis import app
from orbis.libs.entity_type_lib import normalize_entity_type
from orbis.libs.entity_preprocessing_lib import apply_lense
from orbis.libs.entity_preprocessing_lib import apply_filter
from orbis.libs.entity_preprocessing_lib import apply_mapping

import spotlight
import glob
import os


def run(config_dict: dict, data: dict) -> dict:

    computed_path = config_dict["computed_path"]
    corpus_path = config_dict["corpus_path"]
    lense = config_dict["lense"]
    mapping = config_dict["mapping"]
    str_filter = config_dict["str_filter"]

    files = glob.glob(os.path.join(corpus_path, "*.txt"))
    for file_dir in sorted(files, key=lambda name: int(name.split("/")[-1].split(".")[0])):
        app.logger.info("Requesting from Spotlight: {} ({})".format(file_dir.split("/")[-1], corpus_path.split("/data/")[-1].replace("/", "_")))

        file_name = file_dir.split("/")[-1]
        file_number = file_name.split(".")[0]

        cached_file = os.path.abspath(os.path.join(computed_path, file_number + ".json"))
        if os.path.isfile(cached_file):
            app.logger.info("Already received from Spotlight: {}".format(file_dir.split("/")[-1]))
            continue

        with open(file_dir) as open_file:
            response = query(text=open_file.read())

        file_entities = []

        for idx, item in enumerate(response):

            item["key"] = item["URI"]
            item["key"] = item["key"].replace("http://en.wikipedia.org/wiki/", "http://dbpedia.org/resource/")
            item["key"] = item["key"].replace("http://de.dbpedia.org/resource/", "http://dbpedia.org/resource/")

            item["key"] = apply_mapping(mapping, item["key"])

            places = ["place", "location", "settlement"]
            persons = ['http://xmlns.com/foaf/0.1/person', 'person']
            orgs = ["organisation"]
            item["entity_type"] = "NoType"

            for place in places:
                if place in item["types"].lower():
                    item["entity_type"] = normalize_entity_type("location")

            for person in persons:
                if person in item["types"].lower():
                    item["entity_type"] = normalize_entity_type("person")

            for org in orgs:
                if org in item["types"].lower():
                    item["entity_type"] = normalize_entity_type("organisation")

            app.logger.debug("Spotlight Entity Type: {}".format(item["entity_type"]))

            item["document_start"] = int(item["offset"])
            item["document_end"] = int(item["offset"]) + len(item["surfaceForm"])

            in_lense = apply_lense(lense, item["key"])
            to_filter = apply_filter(str_filter, item["surfaceForm"])

            if in_lense or not to_filter:
                file_entities.append(item)

        data[file_number]["computed"] = file_entities

        app.logger.debug("Received from Spotlight: {}".format(file_dir.split("/")[-1]))

    return data


def query(text=None):
    client = 'http://model.dbpedia-spotlight.org/de/annotate'
    only_pol_filter = {
        'policy': 'whitelist',
        'types': 'DBpedia:Person, DBpedia:Place, DBpedia:Location, DBpedia:Organisation, Http://xmlns.com/foaf/0.1/Person',
        'coreferenceResolution': True
    }

    try:
        data = spotlight.annotate(client, text=text, filters=only_pol_filter)
    except spotlight.SpotlightException as error:
        app.logger.error("SpotlightException")
        app.logger.debug("SpotlightException: {}".format(error))
        data = []

    return data
