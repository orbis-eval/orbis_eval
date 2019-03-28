#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


import argparse


def parse_args() -> argparse.Namespace:
    """ Parses the arguments when running Orbis from the console.
    Returns the args (standard to __main__.py)

    :returns: The argparse.Namespace
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-t', '--test', default=False, action='store_true',
                        help='Text input as string. Use \' in console')

    parser.add_argument('-c', '--config', default=False, action='store',
                        help='Define single yml config to run.')

    parser.add_argument('--deletehtml', default=False, action='store_true',
                        help='Delete output html folders.')

    parser.add_argument('--satyanweshi', default=False, action='store_true',
                        help='Build the HTML view of the results.')

    parser.add_argument('-i', '--input', default=False, action='store',
                        help='Build the HTML view of the results.')

    parser.add_argument('--mark-results-below-f1', default=False, action='store',
                        help='Build the HTML view of the results.')

    parser.add_argument('--run-addon', default=False, action='store_true',
                        help='Run a Orbis addon from a list of installed addons.')

    parser.add_argument('--cache', default=False, action='store_true',
                        help='Run Orbis using the webservice cache.')

    parser.add_argument('--recache', default=False, action='store_true',
                        help='Run Orbis rebuilding the webservice cache.')

    args = parser.parse_args()

    return args
