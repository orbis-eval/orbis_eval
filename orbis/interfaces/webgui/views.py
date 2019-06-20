#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from flask import render_template

from .start import app


@app.route('/')
@app.route('/index')
def _index():
    """
    """
    return render_template("index.html")
