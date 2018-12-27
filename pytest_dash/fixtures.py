from __future__ import print_function

import pprint
import threading
import time
import sys
import subprocess
import shlex
import uuid

import six
from selenium.common.exceptions import TimeoutException

try:
    from queue import Queue, Empty
except ImportError:
    # noinspection PyUnresolvedReferences
    from Queue import Queue, Empty

import pytest
import flask
import requests
import percy

from pytest_dash.errors import DashAppLoadingError
from pytest_dash.utils import wait_for_element_by_css_selector


def _stop_server():
    stopper = flask.request.environ['werkzeug.server.shutdown']
    stopper()
    return 'stop'


def _wait_for_client_app_started(driver, url, wait_time=0.5, timeout=10):
    # Wait until the #_dash-app-content element is loaded.
    start_time = time.time()
    loading_errors = (
        'error loading layout',
        'error loading dependencies',
        'Internal Server Error'
    )
    while True:
        try:
            driver.get(url)
            wait_for_element_by_css_selector(
                driver, '#_dash-app-content',
                timeout=wait_time
            )
            return
        except TimeoutException:
            body = wait_for_element_by_css_selector(driver, 'body')
            if any(x in body.text for x in loading_errors) \
                    or time.time() - start_time > timeout:

                logs = driver.get_log('browser')
                raise DashAppLoadingError(
                    'Dash could not start after {}:'
                    ' \nHTML:\n {}\n\nLOGS: {}'.format(
                        timeout,
                        body.get_property('innerHTML'),
                        pprint.pformat(logs)
                    )
                )


@pytest.fixture(scope='package')
def percy_snapshot(selenium):
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
    namespace = {
        'process': None,
        'queue': Queue(),
        'port': 8050
    }

    def _enqueue(out):
        for line in iter(out.readline, b''):
            namespace['queue'].put(line)
        out.close()

    def _sub(app_module, server_instance='app.server', port=8050):
        server_path = '{}:{}'.format(app_module, server_instance)
        namespace['port'] = port

        status = None
        started = False
        is_windows = sys.platform == 'win32'

        cmd = 'waitress-serve --listen=127.0.0.1:{} {}'.format(
            port,
            server_path
        )
        line = shlex.split(cmd, posix=not is_windows)

        # noinspection PyTypeChecker
        process = namespace['process'] = \
            subprocess.Popen(line,
                             bufsize=1,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        queue_thread = threading.Thread(
            target=_enqueue,
            args=(process.stdout,),
        )
        queue_thread.daemon = True
        queue_thread.start()

        while not started and status is None:
            status = process.poll()
            try:
                out = namespace['queue'].get(timeout=.1)
                out = out.decode()
                if 'Serving on' in out:
                    started = True

            except Empty:
                pass

        if status is not None:
            _, err = process.communicate()
            print(err.decode(), file=sys.stderr)
            raise Exception('Could not start the server.')

        url = 'http://localhost:{}/'.format(port)
        _wait_for_client_app_started(selenium, url)

    yield _sub

    namespace['process'].kill()
    while not namespace['process'].poll():
        time.sleep(0.01)
