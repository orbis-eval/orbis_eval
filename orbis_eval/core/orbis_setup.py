# -*- coding: utf-8 -*-

from pathlib import PurePath
from setuptools import find_packages
from setuptools import setup
import re
import io
import os
import sys


class OrbisSetupBaseClass(object):
    """docstring for OrbisSetupBaseClass"""

    def __init__(self):
        super(OrbisSetupBaseClass, self).__init__()

    def load_requirements_file(self, plugin_name, metadata, dev):
        # requirements = ["orbis_eval"] if metadata["type"] != "main" else []
        requirements = []
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

    def get_long_description(self):
        with io.open("README.md", "rt", encoding="utf8") as f:
            long_description = f.read()
        return long_description

    def parse_metadata(self, target, file_content):
        regex = f"^{target} = ['\"](.*?)['\"]"
        metadatum = re.search(regex, file_content, re.MULTILINE).group(1)
        return metadatum

    def load_metadata(self, directory, plugin_name):
        metadata = {}

        with io.OpenWrapper(f"{directory}/{plugin_name}/__init__.py", "rt", encoding="utf8") as open_file:
            file_content = open_file.read()

        metadata["version"] = self.parse_metadata("__version__", file_content)
        metadata["name"] = self.parse_metadata("__name__", file_content)
        metadata["author"] = self.parse_metadata("__author__", file_content)
        metadata["description"] = self.parse_metadata("__description__", file_content)
        metadata["license"] = self.parse_metadata("__license__", file_content)
        metadata["min_python_version"] = self.parse_metadata("__min_python_version__", file_content)
        metadata["requirements_file"] = self.parse_metadata("__requirements_file__", file_content)
        metadata["url"] = self.parse_metadata("__url__", file_content)
        metadata["year"] = self.parse_metadata("__year__", file_content)
        metadata["type"] = self.parse_metadata("__type__", file_content)

        return metadata

    def run(self, directory):

        path_split = PurePath(directory).parts
        plugin_name = path_split[-1]

        metadata = self.load_metadata(directory, plugin_name)
        self.check_python_version(metadata)

        dev = False  # Dev set ignores requirements versions

        setup_dict = {
            "name": metadata['name'],
            "author": metadata['author'],
            "version": metadata['version'],
            "description": metadata['description'],
            "long_description": self.get_long_description(),
            "long_description_content_type": 'text/markdown',
            "url": metadata['url'],
            "license": metadata['license'],
            "packages": find_packages(),
            "python_requires": f">{metadata['min_python_version']}",
            "install_requires": self.load_requirements_file(plugin_name, metadata, dev),
            "include_package_data": True
        }

        if metadata["type"] == "main":
            print("Main found. Installing entry points.")
            setup_dict["entry_points"] = {
                'console_scripts': [
                    'orbis = orbis.__main__:run',
                    'orbis-addons = orbis.interfaces.addons.main:run'
                ]
            }

        setup(**setup_dict)


if __name__ == '__main__':
    directory = os.path.dirname(os.path.realpath(__file__))
    OrbisSetupBaseClass().run(directory)
