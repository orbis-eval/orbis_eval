import yaml
import json
import os

from time import sleep
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
from flask import url_for
from webgui import webgui_app
from webgui.webgui_libs import get_config_yaml
from orbis_plugin_storage_html_pages.templates.html_body import html_body

from orbis_eval import app
from orbis_eval.__main__ import run_orbis
from orbis_eval.libs.plugins import load_plugin

from webgui.forms import ConfigForm

webgui_app.secret_key = 'development key'


@webgui_app.route('/config')
def config():
    form = ConfigForm()
    return render_template('evaluation.html', form=form)


# TODO: args url to navigate results
@webgui_app.route('/view/<page_key>')
def view(page_key):
    html_blocks = webgui_app.db['html_blocks']

    return html_body.format(**html_blocks[page_key])


@webgui_app.route('/build_config', methods=['POST'])
def build_config():
    data = request.form.to_dict()
    rucksack = run_orbis(get_config_yaml(data), webgui=True)

    imported_module = load_plugin("storage", "html_pages")
    module_class_object = imported_module.Main
    html_blocks = module_class_object(rucksack).run()
    webgui_app.db['html_blocks'] = html_blocks

    webgui_app.db['block_keys'] = sorted([key for key in webgui_app.db['html_blocks'].keys()])

    return redirect(url_for('view', page_key=webgui_app.db['block_keys'][0]))


if __name__ == '__main__':
    app.run(debug=True)

# @webgui_app.route('/')
# def index():
#    return render_template('index.html')

"""
@webgui_app.route('/stream')
def stream():

    def generate():
        with open('job.log') as f:
            while True:
                yield f.read()
                sleep(1)

    return webgui_app.response_class(generate(), mimetype='text/plain')
"""
