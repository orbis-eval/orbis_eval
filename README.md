[Orbis](../index.html)

2.0

Contents:

-   [Orbis quickstart](#)
-   [Install Orbis](#install-orbis)
    -   [Prerequisites](#prerequisites)
    -   [Install](#install)
    -   [Run](#run)
    -   [Configure evaluation runs](#configure-evaluation-runs)
-   [Welcome to the Orbis developer
    documentation!](../development_guide/index.html)
-   [Indices and
    tables](../development_guide/index.html#indices-and-tables)

** [Orbis](../index.html)

-   [Docs](../index.html) »
-   Orbis quickstart
-   [View page source](../_sources/quickstart/index.rst.txt)

* * * * *

Orbis quickstart[¶](#orbis-quickstart "Permalink to this headline")
===================================================================

Install Orbis[¶](#install-orbis "Permalink to this headline")
=============================================================

Prerequisites[¶](#prerequisites "Permalink to this headline")
-------------------------------------------------------------

To be able to develop and run Orbis you will need the following
installed and configured on your system: - Python 3.6 - Python Setup
Tools

Install[¶](#install "Permalink to this headline")
-------------------------------------------------

To use Orbis, the repository needs to be clone and Orbis has to be
installed on your system.

    $ git clone https://github.com/htwchur/Orbis.git
    $ cd Orbis
    $ python3 setup.py install --user
    # or if you are developing Orbis and don't want to reinstall after every code change:
    $ python3 setup.py develop

Depending on your system and if you have Python 2 and Python 3 installed
you either need use `python3`{.samp .docutils .literal .notranslate}
(like on Ubuntu) or maybe just `python`{.samp .docutils .literal
.notranslate}.

Run[¶](#run "Permalink to this headline")
-----------------------------------------

Configure evaluation runs[¶](#configure-evaluation-runs "Permalink to this headline")
-------------------------------------------------------------------------------------

Orbis uses yaml files to configure the evaluation runs. These config
file are located in the queue folder in the Orbis root directory
`orbis/queue`{.samp .docutils .literal .notranslate}. Executing Orbis in
test mode will run the yaml configs located in the test folder within
the queue folder. These test configs are short evaluation runs for
different annotators (AIDA, Babelfly, Recognyze and Spotlight).

A YAML configuration file is divided into the seperate stages of the
pipeline:

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

-   Aggregation: The aggregation stage of orbis collects all the data
    needed for an evaluation run. This includes corpus, quering the
    annotator and mappings, lenses and filters used by monocle. The
    aggregation settings specify what service, dataset and what lenses,
    mappings and filters should be used.

<!-- -->

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

The service section of the yaml config specifies the name of the web
service (annotation service). This should be the same (written the same)
as the folder of the webservice located in
`orbis/orbis/plugins/aggregation`{.samp .docutils .literal
.notranslate}. Location specifies where the annotations should come
from. If it’s set to web, then the aggregation plugin will attemt to
query the webservice. If location is set to local, then the local cache
(located in
`orbis/data/corpora/corpus_name/copmuted/annotator_name/`{.samp
.docutils .literal .notranslate}) will be used assumed there is a cache
to be used.

    aggregation:
      service:
        name: aida
        location: web

The service section of the yaml config specifies the name of the web
service (annotation service). This should be the same (written the same)
as the folder of the webservice located in
`orbis/orbis/plugins/aggregation`{.samp .docutils .literal
.notranslate}. Location specifies where the annotations should come
from. If it’s set to web, then the aggregation plugin will attemt to
query the webservice. If location is set to local, then the local cache
(located in
`orbis/data/corpora/corpus_name/copmuted/annotator_name/`{.samp
.docutils .literal .notranslate}) will be used assumed there is a cache
to be used. If there is no cache, run the evaluation in web mode and add
`- cache_webservice_results`{.samp .docutils .literal .notranslate} to
the storage section to build a cache.

The input section defines what corpus should be used (in the example
rss1). The corpora name should be written the same as the corpus folder
located in `orbis/data/corpora/`{.samp .docutils .literal .notranslate}.
Orbis will locate from there on automatically the corpus texts and the
gold standard.

    input:
      data_set:
        name: rss1
      lenses:
        - 3.5 -entity_list_en.txt-14dec-0130pm
      mappings:
        - redirects-v2.json-15dec-1121am
      filters:
        - us_states_list_en-txt-12_jan_28-0913am

If needed, the lenses, mappings and filters can also be specified in the
input section. These should be located in
`orbis/data/[filters|lenses|mappings]`{.samp .docutils .literal
.notranslate} and should be specified in the section without the file
ending.

-   Evaluation: The evaluator stage evaluates the the annotator results
    against the gold standard. The evaluation section defines what kind
    of evaluation should be used. The evaluator should have the same
    name the evaluation folder name in
    `orbis/orbis/plugins/evaluation`{.samp .docutils .literal
    .notranslate}. At the moment the

<!-- -->

    evaluation:
      name: binary_classification_evaluation

-   Scoring: The scoring stage scores the evaluation according to
    specified conditions. These conditions are preset in the scorer and
    can be specified in the scoring section as well as what entity types
    should be scored. If no entity type is defined, all are scored. If
    one or more entity types are defined, then only those will be
    scored. Additionally `ignore_empty`{.samp .docutils .literal
    .notranslate} can be set to define if the scorer should ignore empty
    annotation results or not.

<!-- -->

    scoring:
      name: nel_scorer
      condition: overlap
      entities:
        - Person
        - Organization
        - Place
      ignore_empty: False

Currently available conditions are:
:   -   simple: - same url - same entity type - same surface form
    -   strict: - same url - same entity type - same surface form - same
        start - same end
    -   overlap: - same url - same entity type - overlap

-   Metrics: The metrics stage calculates the metrics to analyze the
    evaluation. The defined metrics name should be written the same as
    the folder of the metrics plugin located at
    `orbis/orbis/plugins/metrics/`{.samp .docutils .literal
    .notranslate}.

<!-- -->

    metrics:
      name: binary_classification_metrics

-   Storage: The storage stage defines what kind of output orbis should
    create. As allways, the metrics plugin should be written the same as
    the folder of the metrics plugin defined in
    `orbis/orbis/plugins/storage`{.samp .docutils .literal
    .notranslate}.

<!-- -->

    storage:
      - cache_webservice_results
      - csv_result_list
      - html_pages

Multiple storage options can be chosen and the ones in the example above
are the recomended (at the moment working) possibilities.

Running `orbis -t`{.samp .docutils .literal .notranslate} will run the
test files located in `orbis/queue/tests`{.samp .docutils .literal
.notranslate}. It is possible to just take one of these YAML files and
modify them to your own needs.

[Next](../development_guide/index.html "Welcome to the Orbis developer documentation!")
[Previous](../index.html "Welcome to the Orbis documentation!")

* * * * *

© Copyright 2019,FabianOdoni

Built with [Sphinx](http://sphinx-doc.org/) using a
[theme](https://github.com/rtfd/sphinx_rtd_theme) provided by [Read the
Docs](https://readthedocs.org).
