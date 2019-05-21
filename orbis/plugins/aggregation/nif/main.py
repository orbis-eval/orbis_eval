#!/usr/bin/python3
# -*- coding: utf8 -*-
"""Summary
"""

import urllib
import os
import regex

from rdflib import Graph, Namespace
from SPARQLWrapper import SPARQLWrapper, JSON

from . import config
from . import dbpedia_types


class NIFAggregation(object):
    """docstring for NIFAggregation"""

    def __init__(self, rucksack):
        super(NIFAggregation, self).__init__()
        self.rucksack = rucksack
        self.config = self.rucksack["config"]
        self.data = self.rucksack["data"]
        self.results = self.rucksack["results"]

    def run(self):
        """

        :param data:
        :param self.config:
        :return:

        Args:
            self.config (dict): Description
            data (dict): Description
        """
        self.extract_entities_from_nif_corpus("Reuters-128.ttl", "Reuters-128-Type_Enhanced.test")

    def extract_files_from_nif_corpus(turtle_input, folder):
        """
        Extracts the documents from a NIF corpus/corpora.
        :param turtle_input:
        :param folder: the ouput folder for the corpus
        :returns: -

        Args:
            turtle_input (TYPE): Description
            folder (TYPE): Description
        """
        g = Graph()
        g.parse(turtle_input, format="turtle")

        for subject, predicate, object_ in g.triples((None, nif_namespace.isString, None)):

            document_number = (subject.split("/")[8]).split("#")[0]
            filename = folder + document_number + ".txt"
            if not os.path.exists(filename):
                with open(filename, "w+") as open_file:
                    open_file.write(object_.encode('utf-8'))

    def extract_entities_from_nif_corpus(turtle_input, output_file_name):
        """Summary

        Args:
            turtle_input (TYPE): Description
            output_file_name (TYPE): Description
        """
        g = Graph()
        g.parse(turtle_input, format="turtle")

        with open(output_file_name, "w") as open_file:

            for subject, predicate, object_ in g.triples((None, nif_namespace.anchorOf, None)):

                doc_split = (subject.split("/")[5]).split("#")
                document_number = doc_split[0]
                surfaceForm = object_

                commaSplit = doc_split[1].split(",")
                start = commaSplit[0].split("=")[1]
                end = commaSplit[1]

                subject_2 = subject

                for subject_2, predicate_2, object_2 in g.triples((subject_2, itsrdf_namespace.taIdentRef, None)):
                    link = object_2
                    type_ = get_dbpedia_type('http://dbpedia.org/sparql', link)

                    line = ",".join([document_number, start, end, link.strip(), "1", type_, surfaceForm, "\n"])
                    open_file.write(line)

def main():
    """Summary
    """
    print("start")
    extract_entities_from_nif_corpus("Reuters-128.ttl", "Reuters-128-Type_Enhanced.test")
    print("end")
    print("Entities found: {}".format(found_number))
    print("Entities not found: {}".format(not_found_number))


if __name__ == '__main__':
    main()
