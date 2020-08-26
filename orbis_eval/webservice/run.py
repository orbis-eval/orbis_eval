import os
from flask import Flask, render_template
from orbis_eval.webservice.models.plugins import get_installed_plugins

app = Flask('orbis-eval')


@app.route('/')
def index():
    available_plugins = get_installed_plugins()
    return render_template('index.html', available_plugins=available_plugins)


def start_webservice():
    os.chdir(os.path.dirname(__file__))
    app.run(port=5000, debug=True)
