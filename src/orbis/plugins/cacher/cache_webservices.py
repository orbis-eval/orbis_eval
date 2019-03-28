import os
import inspect
from orbis.interfaces import aggregation
from orbis.config import paths
from glob import glob


def get_corpora_list():
    corpora = [corpus.strip("/").split("/")[-1] for corpus in glob(os.path.join(paths.corpora_dir, "*/"))]
    return corpora


def get_webservice_list():
    aggregators = [aggregator[0].replace("Aggregator", "").lower() for aggregator in inspect.getmembers(aggregation, inspect.isclass)
                   if len(aggregator[0].replace("Aggregator", "")) > 0]
    return aggregators


def main():
    print("Please select a ")


if __name__ == '__main__':
    print(get_corpora_list())
    print(get_webservice_list())
