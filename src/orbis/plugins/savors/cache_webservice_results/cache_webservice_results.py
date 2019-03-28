import os
import json
import orbis.config
from orbis.libs.files_lib import create_folder


def run(yaml_config: dict, data: dict, results: dict):

        data_set_name = yaml_config["aggregator"]["input"]["data_set"]["name"]
        data_set_path = os.path.join(orbis.config.paths.corpora_dir, data_set_name)
        service_name = yaml_config["aggregator"]["service"]["name"]
        path = os.path.join(data_set_path, "computed", service_name)

        create_folder(path)

        for number, item in data.items():
            with open(os.path.join(path, str(number) + ".json"), "w") as open_file:
                json.dump(item["computed"], open_file)
