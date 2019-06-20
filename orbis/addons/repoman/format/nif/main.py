#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from . import convert


def run(file_destination, corpus_dir, file_name):

    if file_name.endswith("ttl"):
        convert.Convert().convert(file_destination, corpus_dir, file_name)
    else:
        convert.Convert().convert(file_destination, corpus_dir, file_name)

