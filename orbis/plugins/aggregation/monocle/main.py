import json
import os
import pickle
import lzma
import html
from urllib.parse import unquote_plus

from orbis import app
from orbis.libs import cli


def build_source_path(file_name: str, resource_type: str) -> str:
    file_path = os.path.abspath(os.path.join(os.path.join(app.paths.data_dir, f"{resource_type}s")))
    source_file = os.path.join(file_path, file_name + ".xz")
    return source_file


@cli.print_loading("lense", with_runtime=True)
def load_lense(file_names: list = False, refresh: bool = False) -> dict:
    file_path = os.path.abspath(os.path.join(os.path.join(app.paths.data_dir, f"{'lense'}s")))
    lense_dict = {}
    for file_name in file_names:
        pickle_file = os.path.join(file_path, file_name + ".pickle")
        source_file = os.path.join(file_path, file_name + ".xz")
        already_converted = os.path.isfile(pickle_file)
        source_available = os.path.isfile(source_file)
        if refresh or not already_converted:
            if not source_available:
                raise RuntimeError(f"No Source to convert found {source_file}")
            app.logger.info("Converting lense to pickle")
            convert_lense(source_file)
        with open(pickle_file, "rb") as pickle_file:
            new_lense_dict = pickle.load(pickle_file)
        lense_dict.update(new_lense_dict)
    return lense_dict


@cli.print_loading("mapping", with_runtime=True)
def load_mapping(file_names=False, refresh=False) -> dict:
    file_path = os.path.abspath(os.path.join(os.path.join(app.paths.data_dir, f"{'mapping'}s")))
    mapping_dict = {}
    for file_name in file_names:
        pickle_file = os.path.join(file_path, file_name + ".pickle")
        source_file = os.path.join(file_path, file_name + ".xz")
        already_converted = os.path.isfile(pickle_file)
        source_available = os.path.isfile(source_file)
        if refresh or not already_converted:
            if not source_available:
                raise RuntimeError(f"No Source to convert found {source_file}")
            app.logger.info("Converting Mapping to pickle")
            convert_mapping(source_file)
        with open(pickle_file, "rb") as pickle_file:
            new_mapping_dict = pickle.load(pickle_file)
        mapping_dict.update(new_mapping_dict)
    return mapping_dict


@cli.print_loading("filter", with_runtime=True)
def load_filter(file_names=False, refresh=False) -> dict:
    file_path = os.path.abspath(os.path.join(os.path.join(app.paths.data_dir, f"{'filter'}s")))
    filter_dict = {}
    for file_name in file_names:
        pickle_file = os.path.join(file_path, file_name + ".pickle")
        source_file = os.path.join(file_path, file_name + ".xz")
        already_converted = os.path.isfile(pickle_file)
        source_available = os.path.isfile(source_file)
        if refresh or not already_converted:
            if not source_available:
                raise RuntimeError(f"No Source to convert found {source_file}")
            app.logger.info("Converting filter to pickle")
            convert_filter(source_file)
        with open(pickle_file, "rb") as pickle_file:
            new_filter_dict = pickle.load(pickle_file)
        filter_dict.update(new_filter_dict)
    return filter_dict


def convert_resources(source_dir: str, resource: str) -> None:
    if resource == "mapping":
        convert_mapping(source_dir)
    if resource == "lense":
        convert_lense(source_dir)
    if resource == "filter":
        convert_filter(source_dir)


def convert_mapping(source_dir: str) -> None:
    entity_map = {}
    with lzma.open(source_dir, "r") as open_file:
        redirects = json.load(open_file)
        redirects_len = len(redirects)
        dict_position = 0
        for source, redirects in redirects.items():
            source = source.replace(" ", "_")
            dict_position += 1
            for redirect in redirects:
                cli.print_progress_bar(dict_position + 1, redirects_len, prefix='Progress:', suffix='Complete', length=50)
                redirect = redirect.replace(" ", "_")
                entity_map["http://dbpedia.org/resource/" + redirect] = "http://dbpedia.org/resource/" + source
            # entity_map[source] = source
    with open(source_dir.rstrip(".xz") + ".pickle", "wb") as open_file:
        pickle.dump(entity_map, open_file, pickle.HIGHEST_PROTOCOL)


def convert_lense(source_dir: str) -> None:
    entity_list_dict = {}
    with lzma.open(source_dir, "r") as open_file:
        entities = open_file.readlines()
        entity_len = len(entities)
        for idx, entity in enumerate(entities):
            cli.print_progress_bar(idx + 1, entity_len, prefix='Progress:', suffix='Complete', length=50)
            entity = entity.decode("utf8")
            entity = html.unescape(entity)
            entity = unquote_plus(entity)
            entity = entity.replace("\n", "")
            entity = entity.replace("http://en.wikipedia.org/wiki/", "http://dbpedia.org/resource/")
            entity = entity.replace(" ", "_")
            entity_list_dict[str(entity)] = True
    with open(source_dir.rstrip(".xz") + ".pickle", "wb") as open_file:
        pickle.dump(entity_list_dict, open_file, pickle.HIGHEST_PROTOCOL)


def convert_filter(source_dir: str) -> None:
    entity_list_dict = {}
    with lzma.open(source_dir, "r") as open_file:
        entities = open_file.readlines()
        entity_len = len(entities)
        for idx, entity in enumerate(entities):
            cli.print_progress_bar(idx + 1, entity_len, prefix='Progress:', suffix='Complete', length=50)
            print(entity)
            entity = str(entity).replace("\n", "")
            entity_list_dict[str(entity)] = True
    with open(source_dir.rstrip(".xz") + ".pickle", "wb") as open_file:
        pickle.dump(entity_list_dict, open_file, pickle.HIGHEST_PROTOCOL)


def check_resources(configs, refresh=False):
    app.logger.info("Checking for resources")
    resource_file_names = {"lenses": [], "mappings": [], "filters": []}
    for config in configs:
        app.logger.debug("Loading config file: {}".format(config["file_name"]))
        for resource_type in ["lenses", "mappings", "filters"]:
            app.logger.debug("Working on: {}".format(resource_type))
            pickel_file_ending = ".pickle"
            # source_file_ending = ".txt" if resource_type == "filters" else ".xz"
            source_file_ending = ".xz"
            if config["aggregation"]["input"].get(resource_type):
                file_path = os.path.abspath(os.path.join(os.path.join(app.paths.data_dir, "{}".format(resource_type))))
                for file_name in config["aggregation"]["input"][resource_type]:
                    pickle_file = os.path.abspath(os.path.join(file_path, file_name + pickel_file_ending))
                    source_file = os.path.abspath(os.path.join(file_path, file_name + source_file_ending))
                    already_converted = os.path.isfile(pickle_file)
                    source_available = os.path.isfile(source_file)
                    if refresh or not already_converted:
                        if refresh:
                            app.logger.debug("Reconverting {} because of refresh request".format(resource_type))
                        if not already_converted:
                            app.logger.debug("Reconverting {} because pickle not found: {}".format(resource_type, pickle_file))
                        if not source_available:
                            # msg = "No Source to convert found: {}".format(config["aggregation"]["input"].get(resource_type))
                            msg = "No Source to convert found: {}".format(source_file)
                            raise RuntimeError(msg)
                        app.logger.debug("Converting {} to pickle: {}".format(resource_type, source_file))
                        convert_resources(source_file, resource_type)
                    else:
                        app.logger.debug("Pickle for {} found".format(resource_type))
                resource_file_names[resource_type].append(file_name)
            else:
                app.logger.debug("No {} resources needed: {}".format(resource_type, config["file_name"]))
    if len(resource_file_names["lenses"]) >= 0:
        file_names = resource_file_names["lenses"]
        app.lenses = load_lense(file_names=file_names)
    else:
        app.logger.debug("No lenses needed for {}".format(config["file_name"]))
    if len(resource_file_names["mappings"]) >= 0:
        file_names = resource_file_names["mappings"]
        app.mappings = load_mapping(file_names=file_names)
    else:
        app.logger.debug("No mappings needed for {}".format(config["file_name"]))
    if len(resource_file_names["filters"]) >= 0:
        file_names = resource_file_names["filters"]
        app.filters = load_filter(file_names=file_names)
    else:
        app.logger.debug("No filters needed for {}".format(config["file_name"]))


def apply_lense(lense: dict, key: str) -> bool:
    in_lense = True
    if lense and key not in lense:
        app.logger.debug(f"Not in lense: {key}")
        in_lense = False
    return in_lense


def apply_filter(str_filter: dict, surface_form: str) -> bool:
    in_filter = False
    if str_filter and surface_form in str_filter:
        app.logger.debug("{} will be filtered".format(surface_form))
        in_filter = True
    return in_filter


def apply_mapping(mapping: dict, key: str) -> str:
    if mapping and mapping.get(key):
        app.logger.debug(f"{key} remapped to {mapping[key]}")
        key = mapping[key]
    return key
