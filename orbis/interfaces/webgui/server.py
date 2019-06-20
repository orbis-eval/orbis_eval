#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

from . import views


def start(threaded=True, host='0.0.0.0', port=5000):
    app.run(threaded=threaded, host=host, port=port)


if __name__ == '__main__':
    start()
