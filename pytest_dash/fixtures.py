"""Pytest fixtures for Dash."""
from __future__ import print_function

import time
import sys
import subprocess
import shlex

import pytest
import flask
import percy

from pytest_dash.errors import DashAppLoadingError
from pytest_dash.utils import _wait_for_client_app_started
from pytest_dash.application_starters import DashThreaded


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

    with DashThreaded(selenium) as starter:
        yield starter


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
