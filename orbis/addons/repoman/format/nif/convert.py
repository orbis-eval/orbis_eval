#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from rdflib import Namespace, Graph
import os
import pathlib

from orbis.plugins.aggregation import dbpedia_entity_types


class Convert(object):
    """docstring for Convert"""

    def __init__(self):
        super(Convert, self).__init__()
        self.nif_namespace = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
        self.itsrdf_namespace = Namespace("http://www.w3.org/2005/11/its/rdf#")

    def convert(self, download_destination, corpus_dir, download_name):
        g = Graph()
        g.parse(download_destination, format="turtle")
        self.extract_files_from_nif_corpus(g, os.path.join(corpus_dir, "corpus"))
        self.extract_entities_from_nif_corpus(g, os.path.join(corpus_dir, "gold"), f"{download_name}.gs")

    def extract_files_from_nif_corpus(self, g, folder):
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        for subject, predicate, object_ in g.triples((None, self.nif_namespace.isString, None)):
            document_number = (subject.split("/")[-1]).split("#")[0]
            filename = os.path.join(folder, document_number + ".txt")

            if not os.path.exists(filename):
                with open(filename, "w", encoding="utf-8") as open_file:
                    open_file.write(object_)

    def extract_entities_from_nif_corpus(self, g, folder, file_name):
        pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(folder, file_name), "w") as open_file:

            for subject, predicate, object_ in g.triples((None, self.nif_namespace.anchorOf, None)):
                subject_id = subject.split("/")[-1]
                document_number, postition = subject_id.split("#")
                start, end = postition.split("=")[-1].split(",")
                surfaceForm = object_
                subject_2 = subject

                for subject_2, predicate_2, object_2 in g.triples((subject, self.itsrdf_namespace.taIdentRef, None)):
                    type_ = dbpedia_entity_types.get_dbpedia_type(object_2)

                    line = "\t".join([document_number, start, end, object_2.strip(), "1", type_, surfaceForm])
                    open_file.write(line + "\n")

