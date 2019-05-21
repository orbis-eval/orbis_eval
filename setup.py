#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
import setuptools
import sys


def load_metadata():
    global __version__, __version_tag__, __project__, __author__
    global __year__, __copyright__, __release__, __license__
    global __description__, __url__
    global __min_python_version__, __requirements_file__

    metadata_dict = {}
    with open("metadata.txt", encoding="utf-8") as open_file:
        for line in open_file.readlines():
            key, value = line.split(" = ")
            metadata_dict[key] = value.replace('"', '').replace("\n", "")

    __version__ = metadata_dict["__version__"]
    __version_tag__ = metadata_dict["__version_tag__"]
    __project__ = metadata_dict["__project__"]
    __author__ = metadata_dict["__author__"]
    __license__ = metadata_dict["__license__"]
    __description__ = metadata_dict["__description__"]
    __url__ = metadata_dict["__url__"]
    __min_python_version__ = metadata_dict["__min_python_version__"]
    __requirements_file__ = metadata_dict["__requirements_file__"]

    metadata_dict["__year__"] = __year__ = datetime.today().year
    metadata_dict["__copyright__"] = __copyright__ = f'{__year__}, {__author__}'
    metadata_dict["__release__"] = __release__ = " ".join([__version__, __version_tag__])

    with open("metadata.txt", "w", encoding="utf-8") as open_file:
        for key, value in metadata_dict.items():
            open_file.write(f'{key} = "{value}"\n')


def load_requirements_file():
    requirements = []
    with open(__requirements_file__, encoding="utf8") as open_file:
        for line in open_file.readlines():
            requirements.append(line.replace("\n", ""))

    return requirements


def check_python_version():
    python_needed = tuple([int(i) for i in __min_python_version__.split(".")])
    if not sys.version_info >= python_needed:
        sys.exit(f"Sorry, Python {__min_python_version__} or newer needed")


def run_setup():
    load_metadata()
    check_python_version()
    setuptools.setup(
        name=__project__,
        version=__version__,
        description=__description__,
        url=__url__,
        license=__license__,
        packages=setuptools.find_packages(),
        python_requires=f">={__min_python_version__}",
        install_requires=load_requirements_file(),
        entry_points={
            'console_scripts': [
                'orbis = orbis.__main__:main'
            ]
        },
    )


if __name__ == '__main__':
    run_setup()
