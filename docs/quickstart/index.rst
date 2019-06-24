Orbis quickstart
================


Install Orbis
==========================

Prerequisites
-------------
To be able to develop and run Orbis you will need the following installed and
configured on your system:
- Python 3.6
- Python Setup Tools


Install
-------
To use Orbis, the repository needs to be clone and Orbis has to be installed on your system.

.. code-block:: shell

    $ git clone https://github.com/htwchur/Orbis.git
    $ cd Orbis
    $ python3 setup.py develop --user

Depending on your system and if you have Python 2 and Python 3 installed you either need use :samp:`python3` (like on Ubuntu) or maybe just :samp:`python`.

Run
---

After installation Orbis can be executed by running :samp:`orbis`. The Orbis help can be be called by using :samp:`-h` (:samp:`orbis -h`).
Before you can run an evaluation, please install a corpus using the repoman addon :samp:`orbis-addons`.

Configure evaluation runs
-------------------------
Orbis uses yaml files to configure the evaluation runs. These config file are located in the queue folder in the Orbis root directory :samp:`orbis/queue`.
Executing Orbis in test mode will run the yaml configs located in the test folder within the queue folder. These test configs are short evaluation runs for different annotators (AIDA, Babelfly, Recognyze and Spotlight).

A YAML configuration file is divided into the seperate stages of the pipeline:

.. code-block:: yaml

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

- Aggregation: The aggregation stage of orbis collects all the data needed for an evaluation run. This includes corpus, quering the annotator and mappings, lenses and filters used by monocle. The aggregation settings specify what service, dataset and what lenses, mappings and filters should be used.

.. code-block:: yaml

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

The service section of the yaml config specifies the name of the web service (annotation service). This should be the same (written the same) as the folder of the webservice located in :samp:`orbis/orbis/plugins/aggregation`.
Location specifies where the annotations should come from. If it's set to web, then the aggregation plugin will attemt to query the webservice. If location is set to local, then the local cache (located in :samp:`orbis/data/corpora/{corpus_name}/copmuted/{annotator_name}/`) will be used assumed there is a cache to be used.

.. code-block:: yaml

    aggregation:
      service:
        name: aida
        location: web

The service section of the yaml config specifies the name of the web service (annotation service). This should be the same (written the same) as the folder of the webservice located in :samp:`orbis/orbis/plugins/aggregation`.
Location specifies where the annotations should come from. If it's set to web, then the aggregation plugin will attemt to query the webservice. If location is set to local, then the local cache (located in :samp:`orbis/data/corpora/{corpus_name}/copmuted/{annotator_name}/`) will be used assumed there is a cache to be used.
If there is no cache, run the evaluation in web mode and add :samp:`- cache_webservice_results` to the storage section to build a cache.

The input section defines what corpus should be used (in the example rss1). The corpora name should be written the same as the corpus folder located in :samp:`orbis/data/corpora/`.
Orbis will locate from there on automatically the corpus texts and the gold standard.

.. code-block:: yaml

    input:
      data_set:
        name: rss1
      lenses:
        - 3.5 -entity_list_en.txt-14dec-0130pm
      mappings:
        - redirects-v2.json-15dec-1121am
      filters:
        - us_states_list_en-txt-12_jan_28-0913am

If needed, the lenses, mappings and filters can also be specified in the input section. These should be located in :samp:`orbis/data/[filters|lenses|mappings]` and should be specified in the section without the file ending.


- Evaluation: The evaluator stage evaluates the the annotator results against the gold standard. The evaluation section defines what kind of evaluation should be used. The evaluator should have the same name the evaluation folder name in :samp:`orbis/orbis/plugins/evaluation`. At the moment the

.. code-block:: yaml

    evaluation:
      name: binary_classification_evaluation


- Scoring: The scoring stage scores the evaluation according to specified conditions. These conditions are preset in the scorer and can be specified in the scoring section as well as what entity types should be scored. If no entity type is defined, all are scored. If one or more entity types are defined, then only those will be scored. Additionally :samp:`ignore_empty` can be set to define if the scorer should ignore empty annotation results or not.

.. code-block:: yaml

    scoring:
      name: nel_scorer
      condition: overlap
      entities:
        - Person
        - Organization
        - Place
      ignore_empty: False

Currently available conditions are:
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

- Metrics: The metrics stage calculates the metrics to analyze the evaluation. The defined metrics name should be written the same as the folder of the metrics plugin located at :samp:`orbis/orbis/plugins/metrics/`.

.. code-block:: yaml

    metrics:
      name: binary_classification_metrics


- Storage: The storage stage defines what kind of output orbis should create. As allways, the metrics plugin should be written the same as the folder of the metrics plugin defined in :samp:`orbis/orbis/plugins/storage`.

.. code-block:: yaml

    storage:
      - cache_webservice_results
      - csv_result_list
      - html_pages

Multiple storage options can be chosen and the ones in the example above are the recomended (at the moment working) possibilities.

Running :samp:`orbis -t` will run the test files located in :samp:`orbis/queue/tests`. It is possible to just take one of these YAML files and modify them to your own needs.

Addons
======

To run an Orbis addon Orbis provides a CLI that can be accessed by running :samp:`orbis-addons` or :samp:`orbis --run-addon`. The menu will guide you to the addons and the addons mostly provide an own menu. Please be aware, that not all addons are working with the newest version of Orbis yet.
