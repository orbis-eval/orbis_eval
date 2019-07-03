from datetime import datetime
from pathlib import PurePath
from setuptools import find_packages
from setuptools import setup
import importlib
import os
import sys


class AddonSetupBaseClass(object):
    """docstring for AddonSetupBaseClass"""

    def __init__(self):
        super(AddonSetupBaseClass, self).__init__()

    def run_additional_setup(self, addon_name):
        add_setup = False
        try:
            add_setup = importlib.import_module(f"{addon_name}.additional_setup")
        except Exception as exception:
            add_setup = False
            print(exception)
            pass

        if add_setup:
            add_setup.run()

    def load_metadata(self):
        metadata = {}
        with open("metadata.txt", encoding="utf-8") as open_file:
            for line in open_file.readlines():
                key, value = line.split(" = ")
                metadata[key] = value.replace('"', '').replace("\n", "")
        metadata['year'] = datetime.today().year
        metadata['copyright'] = f"{metadata['year']}, {metadata['author']}"
        metadata['release'] = " ".join([metadata['version'], metadata['version_tag']])
        with open("metadata.txt", "w", encoding="utf-8") as open_file:
            output_list = []
            for key, value in metadata.items():
                output_list.append((key, value))
            for key, value in sorted(output_list):
                open_file.write(f'{key} = "{value}"\n')
        return metadata

    def load_requirements_file(self, metadata, dev):
        # Why the dev again?
        requirements = ["orbis"]
        with open(metadata['requirements_file'], encoding="utf8") as open_file:
            for line in open_file.readlines():
                if dev:
                    line = line.replace("\n", "").replace("<", "=").replace(">", "=")
                    line = line.split("=")[0]
                    requirements.append(line)
                else:
                    requirements.append(line.replace("\n", ""))
        return requirements

    def check_python_version(self, metadata):
        python_needed = tuple([int(i) for i in metadata['min_python_version'].split(".")])
        if not sys.version_info >= python_needed:
            sys.exit(f"Sorry, Python {metadata['min_python_version']} or newer needed")

    def run(self, directory):

        metadata = self.load_metadata()
        self.check_python_version(metadata)

        path_split = PurePath(directory).parts
        addon_name = path_split[-1]
        parts = addon_name.split("_")
        description = f"{parts[2].capitalize()} {parts[1].capitalize()} for {parts[0].capitalize()}"
        dev = True

        setup(
            name=addon_name,
            author=metadata['author'],
            description=description,
            version=metadata['version'],
            license=metadata['license'],
            packages=find_packages(),
            python_requires=f">={metadata['min_python_version']}",
            include_package_data=True,
            install_requires=self.load_requirements_file(metadata, dev)
        )

        self.run_additional_setup(addon_name)


if __name__ == '__main__':
    directory = os.path.dirname(os.path.realpath(__file__))
    AddonSetupBaseClass().run(directory)
