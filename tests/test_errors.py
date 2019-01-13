# pylint: disable=missing-docstring
import dash
import pytest

from pytest_dash.errors import DashAppLoadingError, NoAppFoundError
from pytest_dash.application_runners import import_app


def test_invalid_start_raises(dash_threaded):
    app = dash.Dash(__name__)

    # Start the server without setting the layout.
    with pytest.raises(DashAppLoadingError):
        dash_threaded(app, start_timeout=1)


def test_no_app_found():
    with pytest.raises(NoAppFoundError):
        import_app('test_apps.invalid_app')
