## Pain point of orbis

* To many dynamic loading of modules. Example: https://github.com/orbis-eval/orbis_addon_repoman/blob/6b17b2c63290cf2d6d74c4367557be332e428736/orbis_addon_repoman/corpora/main.py#L110 .Could be done with design patterns.
* Use Sonar to enforce clean coding style
* Integration test to test the most common use cases. 
* Lot of out commented code.
* To many external plugins. This creates in many cases a lot of boilerplate code. Not obvious relations.
* Using a json file for corups and gold document instead of *.gs and *.txt files. More flexible.
* Replace the rucksack dictionaries with classes.
* Use template engine for html storage.
* Rucksack has config stored twice -> config and open
* Use validation rules to test if config file is correct. At the current state the 
* Use _ for private methods
* code duplication -> use more functions...
* Better user workflow for repoman. Example: To many request for file format. Could be automated.