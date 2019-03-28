#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-



from setuptools import setup, find_packages
from sphinx.setup_command import BuildDoc

import sys
if not sys.version_info >= (3, 6):
    sys.exit("Sorry, Python >= 3.6 needed")

name = 'orbis'
version = '1.0'

setup(
    name=name,
    version=version,
    description='Orbis',
    author='Fabian Odoni',
    url='http://www.htwchur.ch/digital-science/forschung-und-dienstleistung/institut-sii.html',
    license="GPL2",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    python_requires=">=3.6",
    install_requires=[
        'palettable==3.1.1',
        'isodate==0.6.0',
        'pyspotlight==0.7.2',
        'Sphinx==1.7.5',
        'regex==2018.2.21',
        'SPARQLWrapper==1.8.2',
        'pyyaml>=4.2b1',
        'requests>=2.20.0'
    ],
    entry_points={
        'console_scripts': [
            'orbis = orbis.__main__:main'
        ]
    }
)

cmdclass = {'build_sphinx': BuildDoc}
