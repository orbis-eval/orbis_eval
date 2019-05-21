#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
External script to access the weblyzard api since the weblyzard client, that is used,
is still written in Python 2.7 whereas Orbis is written in 3.6.

This script must be called via:
````bash
python2.7 recognize_api.py -t "Some text to analyze" -p profile_name_to_be_used
```

This is done utilizing

```python
command = ["python2.7", "recognize_api.py", "-t", "Some text", "-p", "profile_name_to_be_used"]
p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate()

"""

import argparse

from weblyzard_api.client.recognize.ng import Recognize
from weblyzard_api.client.jeremia import Jeremia


def _get_args():
    """ Parses the arguments if script is run directly via console.
    This is made since the Weblyzard APIs are still running on Python 2.7

    Available command line paramenters are:
    -t, --text, (Str), Text input as String. Must be enclosed in '

    -p, --profile_name, (Str), Name of the recognize profile to be used e.g. MAXIMUM.COVERAGE

    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-t', '--text', type=str, default=None,
                        help='Text input as string. Use \' in console')

    parser.add_argument('-p', '--profile_name', type=str,
                        default="DBPEDIA",
                        help='The desired profile name')

    parser.add_argument('-i', '--id', type=str,
                        default=None, help="Document id")

    parser.add_argument('-r', '--remote', default=False,
                        action='store_true')

    args = parser.parse_args()

    return args


def _query_recognize(input_txt, profile_name, limit=0, id_key="orbis_test"):
    """ Queries the recognize webservice and returns the response

    Parameters
    ----------
    input_txt: str
        The text to be send to recognize
    profile_name: str
        The name of the profile that should be used by recognize
    limit: int
        Well whatever recognize uses the limit for. 0 means all
        and is the default setting.
    id_key: str
        Just sending orbis_test at the moment.

    Returns
    -------
    recognize_document: byte
        The recognize document as byte string.
    """

    recognize_client = Recognize()
    jeremia_client = Jeremia()

    document = {"id": id_key,
                "body": input_txt,
                "title": "",
                "format": "text/html",
                "header": {}}

    jeremia_document = jeremia_client.submit_document(document)
    recognize_document = recognize_client.search_document(profile_name=profile_name, document=jeremia_document, limit=limit)

    return recognize_document


def function_test():
    """
    Function to test if the api is working. Runs if the script is called
    without any arguments.
    """
    print("Running function test\n")

    text = """Microsoft is an American multinational corporation \
    headquartered in Redmond, Washington, that develops, manufactures, \
    licenses, supports and sells computer software, consumer electronics \
    and personal computers and services. It was was founded by \
    Bill Gates and Paul Allen on April 4, 1975."""

    profile_name = "DBPEDIA"

    response = _query_recognize(text, profile_name, id_key=111)

    return response


if __name__ == "__main__":

    args = _get_args()

    if args.remote or args.text:
        print(_query_recognize(args.text, args.profile_name, id_key=args.id))
    else:
        print(function_test())
