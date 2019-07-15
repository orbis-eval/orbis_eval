#!/usr/bin/python3
# -*- coding: utf-8 -*-

from webgui import webgui_app

webgui_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# webgui_app.config.from_object('config')
webgui_app.run(debug=True, host='0.0.0.0', port=5000)
