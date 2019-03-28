from orbis import app
from orbis.libs import entity_type_lib
from orbis.libs.entity_preprocessing_lib import apply_lense
from orbis.libs.entity_preprocessing_lib import apply_filter
from orbis.libs.entity_preprocessing_lib import apply_mapping

import ast
import glob
import os
import subprocess
import sys


def run(config_dict: dict, data: dict):
    """

    :param data:
    :param config_dict:
    :return:
    """

    computed_path = config_dict["computed_path"]
    corpus_path = config_dict["corpus_path"]
    profile_name = config_dict["profile_name"]
    lense = config_dict["lense"]
    mapping = config_dict["mapping"]
    str_filter = config_dict["str_filter"]

    files = glob.glob(os.path.join(corpus_path, "*.txt"))
    for file_dir in sorted(files, key=lambda name: int(name.split("/")[-1].split(".")[0])):
        app.logger.info("Requesting from Recognize: {} ({})".format(file_dir.split("/")[-1], corpus_path.split("/data/")[-1].replace("/", "_")))

        file_name = file_dir.split("/")[-1]
        file_number = file_name.split(".")[0]

        file_entities = []

        cached_file = os.path.abspath(os.path.join(computed_path, file_number + ".json"))
        if os.path.isfile(cached_file):
            app.logger.info("Already received from Recognize: {}".format(file_dir.split("/")[-1]))
            continue

        with open(file_dir) as open_file:
            response = query(text=open_file.read(), profile_name=profile_name, doc_id=file_number)

        if len(response["annotations"]) <= 0:
            app.logger.warning("No entities recieved from recognize: {}".format(file_name))
        else:
            app.logger.debug("Number of entities recieved from Recognize: {}".format(len(response["annotations"])))

            app.logger.debug(response["annotations"])
            for idx, item in enumerate(response["annotations"]):
                item["key"] = apply_mapping(mapping, item["key"])

                item["entity_type"] = entity_type_lib.normalize_entity_type(item["entity_type"])
                item["document_start"] = int(item["start"])
                item["document_end"] = int(item["end"])

                in_lense = apply_lense(lense, item["key"])
                to_filter = apply_filter(str_filter, item["surfaceForm"])

                if in_lense or not to_filter:
                    app.logger.debug("Found Entity: {} ({})".format(item["surfaceForm"], item["key"]))
                    file_entities.append(item)

        data[file_number]["computed"] = file_entities

    return data


def query(text=None, profile_name=None, doc_id=None):
    """ Runs the recognize api as a external Python 2.7 script.
    Server url, username and password musst be saved as
    environment variables.

    :param text: The text to be send to recognize
    :param profile_name: The name of the profile that should be used by recognize
    :param doc_id:
    :return: The output of the Python2.7 Recognize API Script as it would be displayed in the console.
    """

    if (not text or not isinstance(text, str) or
            not profile_name or not isinstance(profile_name, str)):
        raise KeyError  # Not clear error...

    executable = sys.modules[__name__].__file__.replace(__file__.split("/")[-1], "weblyzard_recognize_api.py")

    command = ["python2.7", executable, "-t", text, "-p", profile_name]
    if doc_id:
        command.append("-i")
        command.append(doc_id)

    command.append("-r")

    # print("[orbis api] Running external Python 2.7 Script: {}".format(command))

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()

    # multiline_logging(app, output)

    if len(err) > 0:
        app.logger.error("** {}".format(err))
        output = []
    else:
        output = str(output.decode("utf-8"))
        output = ast.literal_eval(output)

    return output
