from webgui import webgui_app
from sqlitedict import SqliteDict
from orbis_eval.config.paths import output_path
import os


def start_flask():
    webgui_app.db = SqliteDict(os.path.join(output_path, 'webgui.sqlite'), autocommit=True)
    webgui_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # webgui_app.config.from_object('config')
    webgui_app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)

    print(f"13: {dir(webgui_app)}")
    webgui_app.db.close()


def start_browser():
    NotImplementedError


if __name__ == '__main__':
    start_flask()
