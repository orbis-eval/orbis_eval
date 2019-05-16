Orbis
=====

A python-based evaluation framework for web services and apis.

### Usage

#### Requirements
Needs Python 3.6

Needs following packages:
- setuptools
- sphinx
- lxml
- palettable
- isodate

#### Installation
Orbis needs to be installed first using following command:

```bash
python3 setup.py develop
```

#### Configuration
In order to run orbis evaluations the evaluation configurations need to be stored in `evaluation_configs/activated` as a `.yaml` file. Configuration files in the `evaluation_configs/available` folder will not be run only store for later usage. The `evaluation_configs/examples` folder holds example yaml configuration files. 

A `yaml` config contains following:

```yaml
aggregator:
  name: RecognizeAggregator
  profile: GENERAL-2
  limit: 0
  service: "web"
  data_set: "data/corpora/reuters128/computed/recognize/"
  lense:
    - "3.5-entity_list_en.txt-14dec-0130pm"
  mapping: 
    - "redirects-v2.json-15dec-1121am"
  filter:
    - "us_states_list_en-txt-12_jan_28-0913am"

evaluator:
  name: RecognizeEvaluator

scorer: 
  name: RecognizeScorerOverlap
  entities: 
    - Person
    - Organization
    - Place
  ignore_empty: false

metrics:
  - F1Score

savor:
  - build_html_pages
  - list_results
```

#### Running evaluations
Orbis is started with following command:

```bash
orbis
```

#### Orbis options
```
  -h, --help            show this help message and exit
  -t, --test            Text input as string. Use ' in console
  -c CONFIG, --config CONFIG
                        Define single yml config to run.
  --deletehtml          Delete output html folders.
  --satyanweshi         Build the HTML view of the results.
  -i INPUT, --input INPUT
                        Build the HTML view of the results.
  --mark-results-below-f1 MARK_RESULTS_BELOW_F1
                        Build the HTML view of the results.
  --run-addon           Run a Orbis addon from a list of installed addons.
  --cache               Run Orbis using the webservice cache.
  --recache             Run Orbis rebuilding the webservice cache.
```

#### Running Satyanweshi
```bash
orbis -b -i new_-_json_items-aida_local_-_Person_Organization_Place_-2018-02-15_18:11:41.json,spotlight_test_-_json_items-spotlight_local_-_Person_Organization_Place_-2018-02-15_18:11:41.json
```
