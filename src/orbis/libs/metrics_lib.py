#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-




def get_precision(true_positive, false_positive, debug_msg=None):
    """Calculates precision based on the number of true positives and false positives.

    :param true_positive:
    :param false_positive:
    :param debug_msg:
    :return:

    :Example:

    >>> get_precision(8, 4)
    0.6666666666666666
    """

    true_positive, false_positive = float(true_positive), float(false_positive)

    try:
        result = (true_positive / (true_positive + false_positive))

    except ZeroDivisionError:
        result = 0

    return result


def get_recall(true_positive, item_sum, debug_msg=None):
    """Calculates recall based on the number of true positives and false positives.


    :param true_positive: The number of all correct hits.
    :param item_sum: The sum of all relevant items (true positives + false negatives)
    :param debug_msg:
    :return:


    :Example:
    >>> get_recall(8, 20) == 0.4
    """

    true_positive, item_sum = float(true_positive), float(item_sum)

    try:
        result = (true_positive / item_sum)
    except ZeroDivisionError:
        result = 0

    return result


def get_f1_score(precision, recall, debug_msg=None):
    """Calculates precision based on the number of true positives and false positives.

    :param precision:
    :param recall:
    :param debug_msg:
    :return:

    >>> precision = 0.6666666666666666
    >>> recall = 0.4
    >>> get_f1_score(precision, recall)
    0.5
    """

    precision, recall = float(precision), float(recall)

    try:
        result = 2 * ((precision * recall) / (precision + recall))
    except ZeroDivisionError:
        result = 0

    return result


def get_true_positive_rate():
    """

    :raises: NotImplemented
    """
    raise NotImplemented


def get_false_positive_rate():
    """

    :raises: NotImplemented
    """
    raise NotImplemented


def get_roc():
    """

    :raises: NotImplemented
    """
    raise NotImplemented
