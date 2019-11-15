from flask import render_template
from flask import request
from . import webgui_app

from orbis_eval import app
from orbis_eval.__main__ import run_orbis
from .forms import ConfigForm

webgui_app.secret_key = 'development key'


@webgui_app.route('/')
def hello():
    return "Helloo"


@webgui_app.route('/config')
def config():
    form = ConfigForm()
    return render_template('evaluation.html', form=form)


@webgui_app.route('/build_config', methods=['POST'])
def build_config():
    data = request.form.to_dict()

    config_data = {
        'aggregation': {
            'service': {
                'name': data['aggregation__service__name'],
                'location': data['aggregation__service__location']
            },
            'input': {
                'data_set': {
                    'name': data['aggregation__input__data_set__name']
                }
            }
        },
        'evaluation': {
            'name': data['evaluation__name']
        },
        'scoring': {
            'name': data['scoring__name'],
            'condition': 'overlap',
            'ignore_empty': False
        },
        'metrics': {
            'name': data['metrics__name'],

        },
        'storage': [data['storage__name']]
    }

    run_orbis(config_data, webgui=True)
    return 'Finished'


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
