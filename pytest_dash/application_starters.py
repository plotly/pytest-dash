import runpy
import shlex
import subprocess
import time
import uuid
import threading
import sys

import flask
import requests

from pytest_dash.errors import NoAppFoundError, DashAppLoadingError
from pytest_dash.utils import _wait_for_client_app_started


def _stop_server():
    stopper = flask.request.environ['werkzeug.server.shutdown']
    stopper()
    return 'stop'


def import_app(app_file):
    """
    Import a dash application from a module.
    The import path is in dot notation to the module.
    The variable named app will be returned.

    *Example*

        >>> app = import_app('my_app.app')

    Will import the application in module `app` of the package `my_app`.

    :param app_file: Path to the app (dot-separated).
    :type app_file: str
    :raise: pytest_dash.errors.NoAppFoundError
    :return: App from module.
    :rtype: dash.Dash
    """
    try:
        app_module = runpy.run_module(app_file)
        app = app_module['app']
    except KeyError:
        raise NoAppFoundError(
            'No dash `app` instance was found in {}'.format(app_file)
        )
    return app


class BaseDashStarter:
    def __init__(self, driver, keep_open=False):
        self.driver = driver
        self.port = 8050
        self.started = False
        self.keep_open = keep_open

    def start(self, *args, **kwargs):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.start(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.started and not self.keep_open:
            self.stop()

    @property
    def url(self):
        return 'http://localhost:{}'.format(self.port)


class DashThreaded(BaseDashStarter):
    def __init__(self, driver, keep_open=False):
        super(DashThreaded, self).__init__(driver, keep_open=keep_open)
        self.stop_route = '/_stop-{}'.format(uuid.uuid4().hex)

    def start(self, app,
              port=8050, start_wait_time=0.5, start_timeout=10, **kwargs):
        app.server.add_url_rule(self.stop_route, self.stop_route, _stop_server)
        self.port = port

        def run():
            app.scripts.config.serve_locally = True
            app.css.config.serve_locally = True
            app.run_server(debug=False, port=port, threaded=True)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        _wait_for_client_app_started(
            self.driver, self.url, start_wait_time, start_timeout
        )
        self.started = True

        return app

    def stop(self):
        requests.get('{}{}'.format(self.url, self.stop_route))


class DashSubprocess(BaseDashStarter):
    def __init__(self, driver, keep_open=False):
        super(DashSubprocess, self).__init__(driver, keep_open=keep_open)
        self.process = None

    def start(self, app_module, server_instance='app.server', port=8050):
        server_path = '{}:{}'.format(app_module, server_instance)
        self.port = port

        is_windows = sys.platform == 'win32'

        cmd = 'waitress-serve --listen=127.0.0.1:{} {}'.format(
            port, server_path
        )
        line = shlex.split(cmd, posix=not is_windows)

        # noinspection PyTypeChecker
        self.process = subprocess.Popen(
            line, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        url = 'http://localhost:{}/'.format(port)

        try:
            _wait_for_client_app_started(self.driver, url)
        except DashAppLoadingError:
            status = self.process.poll()
            out, err = self.process.communicate()
            print(
                '\nDash subprocess: {} Failed with status: {}'.format(
                    cmd, status
                )
            )
            if out:
                print(out.decode(), file=sys.stderr)
            if err:
                print(err.decode(), file=sys.stderr)
            raise
        else:
            self.started = True

    def stop(self):
        self.process.kill()
        while not self.process.poll():
            time.sleep(0.01)
