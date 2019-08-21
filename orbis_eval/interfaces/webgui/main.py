from .webgui import webgui_app


def start_flask():
    webgui_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # webgui_app.config.from_object('config')
    webgui_app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)


def run():
    start_flask()


if __name__ == '__main__':
    start_flask()
