# Orbis quickstart

## Prerequisites
To be able to develop and run Orbis you will need the following installed and
configured on your system:
- Python 3.6
- Python Setup Tools
- A Linux OS (Windows and Mac are untested)


## Install
To use Orbis, the repository needs to be cloned and Orbis has to be installed on your system.

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
After installation Orbis can be executed by running ```orbis```. The Orbis help can be be called by using ```-h``` (```orbis -h```)
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

The service section of the yaml config specifies the name of the web service (annotation service). This should be the same (written the same) as the folder of the webservice located in ```Orbis/orbis/plugins/aggregation```.
Location specifies where the annotations should come from. If it's set to web, then the aggregation plugin will attemt to query the webservice. If location is set to local, then the local cache (located in ```Orbis/data/corpora/{corpus_name}/copmuted/{annotator_name}/```) will be used assumed there is a cache to be used.

``` yaml
    aggregation:
      service:
        name: aida
        location: web
```

The service section of the yaml config specifies the name of the web service (annotation service). This should be the same (written the same) as the folder of the webservice located in ```Orbis/orbis/plugins/aggregation```.
Location specifies where the annotations should come from. If it's set to web, then the aggregation plugin will attemt to query the webservice. If location is set to local, then the local cache (located in ```Orbis/data/corpora/{corpus_name}/copmuted/{annotator_name}/```) will be used assumed there is a cache to be used.
If there is no cache, run the evaluation in web mode and add ```- cache_webservice_results``` to the storage section to build a cache.

The input section defines what corpus should be used (in the example rss1). The corpora name should be written the same as the corpus folder located in ```Orbis/data/corpora/```.
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

If needed, the lenses, mappings and filters can also be specified in the input section. These should be located in ```Orbis/data/[filters|lenses|mappings]``` and should be specified in the section without the file ending.


### Evaluation
The evaluator stage evaluates the the annotator results against the gold standard. The evaluation section defines what kind of evaluation should be used. The evaluator should have the same name the evaluation folder name in ```Orbis/orbis/plugins/evaluation```. At the moment the

```yaml
    evaluation:
      name: binary_classification_evaluation
```

### Scoring
The scoring stage scores the evaluation according to specified conditions. These conditions are preset in the scorer and can be specified in the scoring section as well as what entity types should be scored. If no entity type is defined, all are scored. If one or more entity types are defined, then only those will be scored. Additionally ```ignore_empty``` can be set to define if the scorer should ignore empty annotation results or not.

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
The metrics stage calculates the metrics to analyze the evaluation. The defined metrics name should be written the same as the folder of the metrics plugin located at ```Orbis/orbis/plugins/metrics/```.

```yaml
    metrics:
      name: binary_classification_metrics
```

### Storage
The storage stage defines what kind of output orbis should create. As allways, the metrics plugin should be written the same as the folder of the metrics plugin defined in ```Orbis/orbis/plugins/storage```.

``` yaml
    storage:
      - cache_webservice_results
      - csv_result_list
      - html_pages
```

Multiple storage options can be chosen and the ones in the example above are the recomended (at the moment working) possibilities.

## Test run
Running ```orbis -t``` will run the test files located in ```Orbis/queue/tests```. It is possible to just take one of these YAML files and modify them to your own needs.

### OrbisAddons
To run an Orbis addon Orbis provides a CLI that can be accessed by running ```orbis-addons``` or ```orbis --run-addon```. The menu will guide you to the addons and the addons mostly provide an own menu.
