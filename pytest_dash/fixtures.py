"""Pytest fixtures for Dash."""
from __future__ import print_function

import threading
import time
import sys
import subprocess
import shlex
import uuid

import pytest
import flask
import requests
import percy

from pytest_dash.errors import DashAppLoadingError
from pytest_dash.utils import _wait_for_client_app_started


def _stop_server():
    stopper = flask.request.environ['werkzeug.server.shutdown']
    stopper()
    return 'stop'


@pytest.fixture(scope='package')
def percy_snapshot(selenium):
    """
    Initialize a percy build once per run.
    Take snapshots with the fixtures.
    Finalize the build once per run.

    :param selenium: A selenium fixture.
    :return:
    """
    loader = percy.ResourceLoader(webdriver=selenium)
    percy_runner = percy.Runner(loader=loader)
    percy_runner.initialize_build()

    def take_snapshot(snapshot_name):
        print('Percy Snapshot {}'.format(sys.version.split(' ')[0]))
        percy_runner.snapshot(name=snapshot_name)

    yield take_snapshot

    percy_runner.finalize_build()


@pytest.fixture
def dash_threaded(selenium):
    """
    Start a local dash server in a new thread. Stop the server in teardown.

    :param selenium: A selenium fixture.
    :return:
    """

    stop_route = '/_stop-{}'.format(uuid.uuid4().hex)
    namespace = dict(
        port=8050,
        url='http://localhost:{}',
        started=False,
    )

    def create_app(app, port=8050, start_wait_time=0.5, start_timeout=10):

        app.server.add_url_rule(stop_route, stop_route, _stop_server)
        namespace['port'] = port
        namespace['url'] = namespace['url'].format(port)

        def run():
            app.scripts.config.serve_locally = True
            app.css.config.serve_locally = True
            app.run_server(debug=False, port=port, threaded=True)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        _wait_for_client_app_started(
            selenium, namespace['url'], start_wait_time, start_timeout
        )
        namespace['started'] = True

        return app

    yield create_app

    # Stop the server in teardown
    if namespace['started']:
        requests.get('{}{}'.format(namespace['url'], stop_route))


@pytest.fixture
def dash_subprocess(selenium):
    """
    Start a Dash server with subprocess.Popen and waitress-serve.
    No instance is returned from this fixture.

    :param selenium: A selenium fixture
    :return:
    """
    namespace = {'process': None, 'port': 8050}

    def _sub(app_module, server_instance='app.server', port=8050):
        server_path = '{}:{}'.format(app_module, server_instance)
        namespace['port'] = port

        is_windows = sys.platform == 'win32'

        cmd = 'waitress-serve --listen=127.0.0.1:{} {}'.format(
            port, server_path
        )
        line = shlex.split(cmd, posix=not is_windows)

        # noinspection PyTypeChecker
        process = namespace['process'] = subprocess.Popen(
            line, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        url = 'http://localhost:{}/'.format(port)

        try:
            _wait_for_client_app_started(selenium, url)
        except DashAppLoadingError:
            status = process.poll()
            out, err = process.communicate()
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

    yield _sub

    namespace['process'].kill()
    while not namespace['process'].poll():
        time.sleep(0.01)
