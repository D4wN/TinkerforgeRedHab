from flask import Flask
from flask import request
from flask.templating import render_template

from util.event_logger import EventLogger

import threading


app = Flask(__name__)


# Routes
@app.route("/", methods=['GET'])
def root():
    return render_template('index.html')


class FlaskWebserver(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)

    def stop(self):
        # stop the webserver
        EventLogger.debug("Flask Webserver stopped...")
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def _job(self):
        # start webserver
        app.run(debug=True)
        EventLogger.debug("Flask Webserver running...")


