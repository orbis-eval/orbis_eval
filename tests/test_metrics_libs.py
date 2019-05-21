#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

'''
    .. moduleauthor:: Fabian Odoni fabian.odoni@htwchur.ch
'''


from orbis.lib import metrics_lib

tp = 8
fp = 4
tn = 12
fn = 12


def test_precision():
    """
    """

    assert metrics_lib.get_precision(tp, fp) == 0.6666666666666666


def test_recall():
    """
    """
    assert metrics_lib.get_recall(tp, sum([tp, fn])) == 0.4


def test_get_f1_score():

    precision = metrics_lib.get_precision(tp, fp)
    recall = metrics_lib.get_recall(tp, sum([tp, fn]))

    f1_score = 2 * ((precision * recall) / (precision + recall))
    assert f1_score == 0.5


if __name__ == '__main__':
    test_precision()
    test_recall()
    test_get_f1_score()
