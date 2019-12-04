from flask import Flask
from flask_bootstrap import Bootstrap

webgui_app = Flask(__name__)
Bootstrap(webgui_app)

from . import views
