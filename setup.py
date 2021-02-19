# -*- coding: utf-8 -*-
try:
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    pass

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from pathlib import PurePath


import re
import io
import os
import sys


class OrbisSetup(object):
    """docstring for OrbisSetup"""

    def __init__(self):
        super(OrbisSetup, self).__init__()

    def load_requirements_file(self, plugin_name, metadata, dev):
        requirements = ["orbis_eval"] if metadata["type"] != "main" else []

        with open(metadata['requirements_file'], encoding="utf8") as open_file:

            for line in open_file.readlines():
                if dev:
                    line = line.replace("\n", "").replace(
                        "<", "=").replace(">", "=")
                    line = line.split("=")[0]
                    requirements.append(line)

                else:
                    requirements.append(line.replace("\n", ""))

        return requirements

    def check_python_version(self, metadata):

        python_needed = tuple(
            [int(i) for i in metadata['min_python_version'].split(".")])

        if not sys.version_info >= python_needed:
            sys.exit(
                f"Sorry, Python {metadata['min_python_version']} or newer needed")

    def get_long_description(self):

        with io.open("README.md", "rt", encoding="utf8") as f:
            long_description = f.read()

        return long_description

    def clean_matches(self, match, target):
        bad = ["=[", "= [", "[", "]", "\n", "'", "\""]
        match = match.replace(f"{target}", "")

        for item in bad:
            match = match.replace(item, "")

        while "  " in match:
            match = match.replace("  ", " ")
        return match

    def parse_metadata(self, target, file_content):

        try:
            regex = f"^{target} = ['\"](.*?)['\"]"
            metadatum = re.search(regex, file_content, re.MULTILINE).group(1)

        except Exception as exception:
            print(f">>> {exception}")
            regex = f"^{target}\s*?=\s*?\[\n(?:.*?\n)*?\]"
            metadatum = re.search(regex, file_content, re.MULTILINE).group()
            metadatum = self.clean_matches(metadatum, target)
            metadatum = [item.strip() for item in metadatum.split(",")]
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
        metadata["plugins"] = self.parse_metadata("__plugins__", file_content)
        metadata["addons"] = self.parse_metadata("__addons__", file_content)

        return metadata

    def get_extras(self, metadata):
        """
        orbis_plugin_aggregation_serial_corpus",
        """
        all_extras = metadata['plugins'] + metadata['addons']
        extras = {}

        for plugin in all_extras:
            parts = plugin.split("_")
            # system = parts[0]
            type_ = parts[1]
            stage = parts[2]
            name = "_".join(parts[2:])

            extras["all"] = extras.get("all", []) + [plugin]
            extras[f"all_{type_}s"] = extras.get(f"all_{type_}s", []) + [plugin]
            if type_ != "addon":
                extras[f"all_{stage}s"] = extras.get(f"all_{stage}s", []) + [plugin]
            extras[name] = plugin
        return extras

    def run(self, directory):

        plugin_name = PurePath(directory).parts[-1]
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
            "package_data": {
                'orbis_eval': [
                    'data/orbis_config/settings.json',
                    'data/tests/queue/*',
                    'data/tests/corpora/rss1/computed/**/*',
                    'data/tests/corpora/rss1/**/*',
                    'data/tests/corpora/rss1/source.txt'
                ]
            }
        }

        if metadata["type"] == "main":
            print("Main found. Installing entry points.")
            setup_dict["entry_points"] = {
                'console_scripts': [
                    'orbis-eval = orbis_eval.main:run',
                    'orbis-addons = orbis_eval.interfaces.addons.main:run',
                    'orbis-cli = orbis_eval.interfaces.cli.main:run'
                ]
            }

        setup_dict["extras_require"] = self.get_extras(metadata)

        setup(**setup_dict)


if __name__ == '__main__':
    directory = os.path.dirname(os.path.realpath(__file__))
    OrbisSetup().run(directory)
