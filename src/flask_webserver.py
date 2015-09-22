from flask import Flask
from flask import request
from flask.templating import render_template
import time

from util.event_logger import EventLogger, WebserverLogger

import threading


app = Flask(__name__)

def dump_queue(queue):
    """
    Empties all pending items in a queue and returns them in a list.
    """
    result = []

    for i in iter(queue.get, 'STOP'):
        result.append(i)
    time.sleep(.1)
    return result

# Routes
@app.route("/", methods=['GET'])
def root():
    FlaskWebserver.all_entries.append(dump_queue(WebserverLogger._queue))
    print str(FlaskWebserver.all_entries)
    return render_template('index.html')


class FlaskWebserver(threading.Thread):

    all_entries = []

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        target = self._job

        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self._webserver_logger = WebserverLogger("WebserverLogger", EventLogger.EVENT_LOG_LEVEL)
        self._started = False

    def stop(self):
        if not self._started:
            return

        with app.test_request_context():
            # stop the webserver
            EventLogger.debug("Flask Webserver stopped...")
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

    def _job(self):
        # start webserver
        self._started = True
        app.run(debug=True)
        EventLogger.debug("Flask Webserver running...")