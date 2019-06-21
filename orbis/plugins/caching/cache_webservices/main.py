import os
import inspect
from glob import glob

from orbis.interfaces import aggregation
from orbis.config import paths


class CacheWebservices(object):

    def __init__(self, rucksack):
        super(CacheWebservices, self).__init__()
        return NotImplementedError

    def get_corpora_list(self):
        corpora = [corpus.strip("/").split("/")[-1] for corpus in glob(os.path.join(paths.corpora_dir, "*/"))]
        return corpora

    def get_webservice_list(self):
        aggregators = [aggregator[0].replace("Aggregator", "").lower() for aggregator in inspect.getmembers(aggregation, inspect.isclass)
                       if len(aggregator[0].replace("Aggregator", "")) > 0]
        return aggregators
