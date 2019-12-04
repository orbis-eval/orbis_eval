# -*- coding: utf-8 -*-

from orbis_eval.core import orbis_app

__name__ = "orbis_eval"
__version__ = "2.2.3"
__author__ = "fabod"
__year__ = "2019"
__description__ = "An Extendable Evaluation Pipeline for Named Entity Drill-Down Analysis"
__license__ = "GPL2"
__min_python_version__ = "3.6"
__requirements_file__ = "requirements.txt"
__url__ = "https://orbis-eval.github.io/Orbis/"
__type__ = "main"
__classifiers__= [
    "Framework :: orbis-eval",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3.7",
    ""


]


app = orbis_app.App()
