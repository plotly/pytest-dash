"""Pytest fixtures for Dash."""
from __future__ import print_function

import sys

import pytest
import percy

from pytest_dash.application_starters import DashThreaded, DashSubprocess


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
    with DashSubprocess(selenium) as starter:
        yield starter
