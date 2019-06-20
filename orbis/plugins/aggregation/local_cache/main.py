import glob
import json
import os

from orbis import app
from orbis.plugins.aggregation import dbpedia_entity_types
from orbis.plugins.aggregation import monocle
from orbis.core.aggregation import AggregationBaseClass


class LocalCacheAggregation(AggregationBaseClass):

    def run(self):
        computed_path = self.config['computed_path']
        lense = self.data['lense']
        mapping = self.data['mapping']
        filter_ = self.data['filter']
        computed = {}
        app.logger.debug(f"Serching for cache files in {computed_path}")
        for file_dir in glob.glob(os.path.join(computed_path, '*.json')):
            file_number = file_dir.split('/')[-1].split('.')[0]
            computed[file_number] = []
            with open(file_dir) as open_file:
                app.logger.debug(f"Opening {file_dir}")
                items = json.load(open_file)

                if items:
                    for item in items:

                        item['key'] = monocle.apply_mapping(mapping, item['key'])
                        in_lense = monocle.apply_lense(lense, item['key'])
                        to_filter = monocle.apply_filter(filter_, item['surfaceForm'])
                        item['entity_type'] = dbpedia_entity_types.normalize_entity_type(item['entity_type'])

                        if item.get('entity_metadata'):
                            item['document_start'] = int(item['entity_metadata']['document_index_start'][0])
                            item['document_end'] = int(item['entity_metadata']['document_index_end'][0])

                        if in_lense and not to_filter:
                            computed[file_number].append(item)

        return computed
