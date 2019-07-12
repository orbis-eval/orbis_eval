# Orbis quickstart

Orbis is a versatile framework for performing NEL evaluation analyses. It supports standard metrics such as precision, recall and F1-score and visualizes gold standard and annotator results in the context of the annotated document. Color coding the entities allows experts to quickly identify correct and incorrect annotations and the corresponding links to the KB that are also provided by Orbis. Due to the modular pipeline architecture used by Orbis different stages in the evaluation process can be easily modified, replaced or added.

Results of our first Orbis based drill-down analyses efforts were presented at the SEMANTiCS 2018 Conference in Vienna [Odoni, Kuntschik, Braşoveanu, & Weichselbraun, 2018](https://www.sciencedirect.com/science/article/pii/S1877050918316089).

## Prerequisites
To be able to develop and run Orbis you will need the following installed and
configured on your system:
- Python 3.7
- Python Setup Tools
- A Linux or Mac OS (Windows is untested)


## Install
To use Orbis, download and install it from PyPI:

```shell
    $ python3 -m pip install -U orbis-eval['all'] --user
```

There are more extras options available but we recommend you use the all option. Only use the other options if you really know what you are doing.
```
    - all: Install all extras for Orbis. Recommended option
    - all_plugins: Install only all plugins for Orbis.
    - all_addons: Install only all addons for Orbis.
    - aggregation: Install only all aggregation plugins for Orbis.
    - evaluation: Install only all evaluation plugins for Orbis.
    - metrics: Install only all metrics plugins for Orbis.
    - scoring: Install only all scoring plugins for Orbis.
    - storage: Install only all storage plugins for Orbis.
    - "plugin or addon name": Install only the specified addon or plugin named.
```

Alternatively Orbis can be install by cloning the Repo and installing it manually. Plugins and addons must be installed seperatly.
```shell
    $ git clone https://github.com/orbis-eval/Orbis.git
    $ cd Orbis
    $ python3 setup.py install --user
    # or
    $ python setup.py install --user
```

Depending on your system and if you have Python 2 and Python 3 installed you either need to use ```python3``` (like on Ubuntu) or maybe just ```python```.

You will promted to set an orbis user folder. This folder will contain the evaluation run queue, the logs, the corpora and monocle data, the output and the documentation. Default location will be ```orbis-eval``` in the user's home folder. An alternative location can be specified.

## Run
After installation Orbis can be executed by running ```orbis-eval```. The Orbis help can be be called by using ```-h``` (```orbis-eval -h```)
Before you can run an evaluation, please install a corpus using the repoman addon ```orbis-addons ```.

## Configure evaluation runs
Orbis uses yaml files to configure the evaluation runs. These config file are located in the queue folder in the Orbis root directory ```Orbis/queue```.
Executing Orbis in test mode will run the yaml configs located in the test folder within the queue folder. These test configs are short evaluation runs for different annotators (AIDA, Babelfly, Recognyze and Spotlight).

A YAML configuration file is divided into the seperate stages of the pipeline:

```yaml
  aggregation:
    service:
      name: aida
      location: web
    input:
      data_set:
        name: rss1
      lenses:
        - 3.5-entity_list_en.txt-14dec-0130pm
      mappings:
        - redirects-v2.json-15dec-1121am
      filters:
        - us_states_list_en-txt-12_jan_28-0913am

  evaluation:
    name: binary_classification_evaluation

  scoring:
    name: nel_scorer
    condition: overlap
    entities:
      - Person
      - Organization
      - Place
    ignore_empty: False

  metrics:
    name: binary_classification_metrics

  storage:
    - cache_webservice_results
```

### Aggregation
The aggregation stage of orbis collects all the data needed for an evaluation run. This includes corpus, quering the annotator and mappings, lenses and filters used by monocle. The aggregation settings specify what service, dataset and what lenses, mappings and filters should be used.

```yaml
    aggregation:
      service:
        name: aida
        location: web
      input:
        data_set:
          name: rss1
        lenses:
          - 3.5-entity_list_en.txt-14dec-0130pm
        mappings:
          - redirects-v2.json-15dec-1121am
        filters:
          - us_states_list_en-txt-12_jan_28-0913am
```

The service section of the yaml config specifies the name of the web service (annotation service). This should be the same (written the same) as the webservice plugin minus the ```orbis_plugin_aggregation_``` prefix.

Location specifies where the annotations should come from. If it's set to web, then the aggregation plugin will attemt to query the webservice. If location is set to local, then the local cache (located in ```~/orbis-eval/data/corpora/{corpus_name}/copmuted/{annotator_name}/```) will be used assuming there is a cache to be used.
If there is no cache, run the evaluation in web mode and add ```- cache_webservice_results``` to the storage section to build a cache.

``` yaml
    aggregation:
      service:
        name: aida
        location: web
```


The input section defines what corpus should be used (in the example rss1). The corpora name should be written the same as the corpus folder located in ```~/orbis-eval/data/corpora/```.
Orbis will locate from there on automatically the corpus texts and the gold standard.

```yaml
    input:
      data_set:
        name: rss1
      lenses:
        - 3.5 -entity_list_en.txt-14dec-0130pm
      mappings:
        - redirects-v2.json-15dec-1121am
      filters:
        - us_states_list_en-txt-12_jan_28-0913am
```

If needed, the lenses, mappings and filters can also be specified in the input section. These should be located in ```~/orbis-eval/data/[filters|lenses|mappings]``` and should be specified in the section without the file ending.


### Evaluation
The evaluator stage evaluates the the annotator results against the gold standard. The evaluation section defines what kind of evaluation should be used. The evaluator should have the same name as the evaluation plugin minus the ```orbis_plugin_evaluation_``` prefix.

```yaml
    evaluation:
      name: binary_classification_evaluation
```

### Scoring
The scoring stage scores the evaluation according to specified conditions. These conditions are preset in the scorer and can be specified in the scoring section as well as what entity types should be scored. If no entity type is defined, all are scored. If one or more entity types are defined, then only those will be scored. Additionally ```ignore_empty``` can be set to define if the scorer should ignore empty annotation results or not.
The scorer should have the same name as the scoring plugin minus the ```orbis_plugin_scoring_``` prefix.

```yaml
    scoring:
      name: nel_scorer
      condition: overlap
      entities:
        - Person
        - Organization
        - Place
      ignore_empty: False
```

Currently available conditions are:

```
  - simple:
    - same url
    - same entity type
    - same surface form

  - strict:
    - same url
    - same entity type
    - same surface form
    - same start
    - same end

  - overlap:
    - same url
    - same entity type
    - overlap
```

### Metrics
The metrics stage calculates the metrics to analyze the evaluation. The metric should have the same name as the metrics plugin minus the ```orbis_plugin_metrics_``` prefix.


```yaml
    metrics:
      name: binary_classification_metrics
```

### Storage
The storage stage defines what kind of output orbis should create. As allways, the storage should have the same name as the storage plugin minus the ```orbis_plugin_storage_``` prefix.


``` yaml
    storage:
      - cache_webservice_results
      - csv_result_list
      - html_pages
```

Multiple storage options can be chosen and the ones in the example above are the recomended (at the moment working) possibilities.

## Test run
Running ```orbis-eval -t``` will run the test files located in ```~/orbis-eval/queue/tests```. It is possible to just take one of these YAML files and modify them to your own needs.

### OrbisAddons
To run an Orbis addon Orbis provides a CLI that can be accessed by running ```orbis-addons``` or ```orbis-eval --run-addon```. The menu will guide you to the addons and the addons mostly provide an own menu.

Orbis addons can be called directly by appending the Addon name the orbis-addon command:
```orbis-addon repoman```
