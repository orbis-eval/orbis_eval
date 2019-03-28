#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-


from orbis.libs.orbis_lib import start_orbis
from orbis.libs.arguments_lib import parse_args


def main():
    """

    :return:
    """

    args = parse_args()
    start_orbis(args)


if __name__ == '__main__':
    main()
