from orbis.libs import files_lib

import os


def run(yaml_config: dict, data: dict, results: dict) -> None:
    return False
    directory_name = files_lib.build_file_name("html", yaml_config)
    files_lib.create_folder(directory_name)

    try:
        os.makedirs(directory_name)
    except Exception:
        pass

    file_dir = os.path.join(directory_name, "index.html")
    with open(file_dir, "w") as open_file:
        open_file.write("html")
