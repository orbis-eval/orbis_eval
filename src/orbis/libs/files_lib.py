import pathlib
import os
import datetime
from orbis.config import paths


def get_timestamp():
    return "{:%Y-%m-%d_%H:%M:%S}".format(datetime.datetime.now())


def create_folder(path: str=None):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def build_file_name(file_name, config, raw=False):
    """

    :param file_name:
    :param config:
    :param raw:
    :return:
    """

    aggregator_name = config["aggregator"]["service"]["name"]
    aggregator_source = config["aggregator"]["service"]["location"]

    if raw:
        file_name = os.path.join(paths.output_path, file_name)

    elif file_name[-1] == "/":
        file_name = config["file_name"].split(".")[0]
        file_name = f"{file_name}_{get_timestamp()}"
        file_name = os.path.join(paths.output_path, file_name)

    else:
        try:
            file_name, ending = file_name.split(".")
            run_name = config["file_name"].split(".")[0]
            source = f'{aggregator_name}_{aggregator_source}_'
            entities = "_{}_".format("_".join(config["scorer"]["entities"]))
            file_name = "{}_-_{}-{}-{}-{}.{}".format(run_name, file_name, source, entities, get_timestamp(), ending)
            file_name = os.path.join(paths.output_path, file_name)

        except ValueError:
            file_name = f'{file_name}_{"-".join(config["scorer"]["entities"])}'
            file_name = f"{file_name}_{get_timestamp()}"
            file_name = os.path.join(paths.output_path, file_name)
    return file_name
