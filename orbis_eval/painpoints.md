## Pain point of orbis

* To many dynamic loading of modules. Example: https://github.com/orbis-eval/orbis_addon_repoman/blob/6b17b2c63290cf2d6d74c4367557be332e428736/orbis_addon_repoman/corpora/main.py#L110 .Could be done with design patterns.
* Use Sonar to enforce clean coding style
* Integration test to test the most common use cases. 
* Lot of out commented code.
* To many external plugins. This creates in many cases a lot of boilerplate code. Not obvious relations.
* Using a json file for corups and gold document instead of *.gs and *.txt files. More flexible.
* Replace the rucksack dictionaries with classes.
* Use template engine for html storage.