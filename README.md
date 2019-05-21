Orbis
=====

A python-based evaluation framework for web services and apis.

### Usage

#### Requirements
Needs Python 3.6
Needs following packages:
  - palettable 3.1.1
  - isodate 0.6.0
  - pyspotlight 0.7.2
  - Sphinx 1.7.5
  - regex 2018.2.21
  - SPARQLWrapper 1.8.2
  - pyyaml 4.2b1
  - requests 2.20.0

#### Installation
Orbis needs to be installed first using following command:

```bash
python3 setup.py develop
```

#### Configuration
In order to run orbis evaluations the evaluation configurations need to be stored in `evaluation_configs/activated` as a `.yaml` file. Configuration files in the `evaluation_configs/available` folder will not be run only store for later usage. The `evaluation_configs/examples` folder holds example yaml configuration files.

A `yaml` config contains following:

```yaml

```

#### Running evaluations
Orbis is started with following command:

```bash
orbis
```

#### Orbis options
```
  -h, --help            show this help message and exit
```
