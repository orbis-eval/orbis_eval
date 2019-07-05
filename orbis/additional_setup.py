import json
from distutils.dir_util import copy_tree
from pathlib import Path
from setuptools.command.install import install


def write_settings(user_dir, settings_dict):
    with open('orbis/config/settings.json', 'r', encoding='utf-8') as settings_file:
        settings = json.load(settings_file)

    settings['user_dir'] = str(user_dir)
    settings.update(settings)
    with open('orbis/config/settings.json', 'w', encoding='utf-8') as settings_file:
        json.dump(settings, settings_file, indent=4)


def create_orbis_external_folder():
    default_dir = Path.home() / "orbis-eval"
    print("Where would you like to install the Orbis input/output directory?")
    user_dir = input(f"> ({str(default_dir)}):") or default_dir
    Path(user_dir).mkdir(parents=True, exist_ok=True)
    settings_dict = {'user_dir': str(user_dir)}
    write_settings(user_dir, settings_dict)
    return user_dir


def fill_data(user_dir):
    source = Path("data")
    target = user_dir / "data"

    copy_tree(str(source), str(target))


def fill_queue(user_dir):
    source = Path("queue")
    target = user_dir / "queue"
    copy_tree(str(source), str(target))


def run():
        user_dir = create_orbis_external_folder()
        fill_data(user_dir)
        fill_queue(user_dir)
        install.run()
