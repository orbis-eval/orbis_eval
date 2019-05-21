#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

'''
    .. moduleauthor:: Fabian Odoni fabian.odoni@htwchur.ch
'''

import os
import json
from orbis.lib import scorer_lib
from orbis.config import paths

test_cases = {
    "0": {
        "gold_path": os.path.abspath(os.path.join(paths.tests_dir, "libs", "scorer_lib", "corpus", "gold_0.json")),
        "calculated_path": os.path.abspath(os.path.join(paths.tests_dir, "libs", "scorer_lib", "corpus", "calculated_0.json")),
        "conditions": ["overlap", "same_url", "same_type"],
        "result": {
            'tp': [1, 0, 0, 1, 0, 0],
            'fp': [0, 0, 0, 0, 0, 1],
            'fn': [0, 1, 1, 0, 1, 0],
            'tp_ids': ['0,25', '401,413'],
            'fp_ids': ['54,88'],
            'fn_ids': ['54,88', '309,331', '420,442'],
            'tp_sum': 2,
            'fp_sum': 1,
            'fn_sum': 3
        }
    },
}
"""
    "1": { Document 46  false positive
        ""
    }
"""


def test_get_confusion_matrix():

    for key, case in test_cases.items():
        with open(case["gold_path"]) as open_file:
            gold = json.load(open_file)
        with open(case["calculated_path"]) as open_file:
            calculated = json.load(open_file)

        result = scorer_lib.get_confusion_matrix(calculated, gold, case["conditions"])
        assert result == case["result"]


if __name__ == '__main__':
    test_get_confusion_matrix()


"""
    gold_path = os.path.abspath(os.path.join(tests_dir, "libs", "scorer_lib", "corpus", "gold_0.json"))
    computed_path = os.path.abspath(os.path.join(tests_dir, "libs", "scorer_lib", "corpus", "computed_0.json"))
    conditions = ["overlap", "same_url", "same_type"]

    with open(gold_path) as open_file:
        gold = json.load(open_file)

    with open(computed_path) as open_file:
        computed = json.load(open_file)
    result_0 = get_confusion_matrix(computed, gold, conditions)

    with open(gold_path) as open_file:
        gold = json.load(open_file)

    with open(computed_path) as open_file:
        computed = json.load(open_file)
    result_1 = get_confusion_matrix(computed, gold, conditions)

    print(result_0)
    print(result_1)
    print("{}\t{}".format(result_0["tp"], result_0["fp"]))
    print("{}\t{}\t{}".format(result_1["tp"], result_1["fp"], result_1["fn"]))


"""
"""
0,25 0,25 1
54,88 False 0
309,331 False 0
401,418 401,413 1
420,442 False 0
False 54,88 0
"""
