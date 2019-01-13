"""
Pytest-dash plugin
------------------
Main entry point for pytest

- Hooks definitions
- Plugin config container
- Plugin selenium driver
- Fixtures imports
"""
import pytest

from selenium import webdriver

from pytest_dash.behaviors import DashBehaviorTestFile
from pytest_dash.errors import InvalidDriverError
from pytest_dash.application_runners import DashThreaded, DashSubprocess


_DRIVER_MAP = {
    'Chrome': webdriver.Chrome,
    'Firefox': webdriver.Firefox,
    'Remote': webdriver.Remote,
    'Safari': webdriver.Safari,
    'Opera': webdriver.Opera,
}


def _create_config(parser, key, help=None):
    # Create an option for pytest command line and ini
    parser.addoption('--{}'.format(key), help=help)
    parser.addini(key, help=help)


def _get_config(config, key, default=None):
    opt = config.getoption(key)
    ini = config.getini(key)
    return opt or ini or default

################################################################################
# Plugin hooks.
################################################################################


def pytest_addoption(parser):
    # Add options to the pytest parser, either on the commandline or ini
    # TODO add more options for the selenium driver.
    _create_config(parser, 'webdriver', 'Name of the selenium driver to use')


def pytest_configure(config):
    # Called once before the tests are run
    # Get and configure global objects for the plugin to use.
    # TODO get all the options and map a global dict.
    driver_name = _get_config(config, 'webdriver')

    if driver_name not in _DRIVER_MAP:
        raise InvalidDriverError(
            '{} is not a valid webdriver value.\n'
            'Valid drivers {}'.format(driver_name, _DRIVER_MAP.keys())
        )

    driver = _DRIVER_MAP.get(driver_name)()

    DashPlugin.driver = driver


def pytest_unconfigure(config):
    # Quit the selenium driver once all tests are cleared.
    DashPlugin.driver.quit()


def pytest_collect_file(parent, path):
    if path.ext == ".yml" and path.basename.startswith("test"):
        return DashBehaviorTestFile(path, parent, DashPlugin)


################################################################################
# Fixtures
################################################################################


@pytest.fixture
def dash_threaded():
    """
    Start a local dash server in a new thread. Stop the server in teardown.

    :return:
    """

    with DashThreaded(DashPlugin.driver) as starter:
        yield starter


@pytest.fixture
def dash_subprocess():
    """
    Start a Dash server with subprocess.Popen and waitress-serve.
    No instance is returned from this fixture.

    :return:
    """
    with DashSubprocess(DashPlugin.driver) as starter:
        yield starter


class DashPlugin:
    """Global plugin configuration and driver container"""
    driver = None
    configs = {}
