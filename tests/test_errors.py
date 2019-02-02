# pylint: disable=missing-docstring
import pytest

from pytest_dash.errors import DashAppLoadingError, NoAppFoundError
from pytest_dash.application_runners import import_app


def test_invalid_start_raises_threaded(dash_threaded):

    # Start the server without setting the layout.
    with pytest.raises(DashAppLoadingError):
        dash_threaded(import_app('test_apps.no_layout_app'), start_timeout=1)


def test_invalid_start_raises_subprocess(dash_subprocess):

    with pytest.raises(DashAppLoadingError):
        dash_subprocess('test_apps.no_layout_app', port=8051)


def test_no_app_found():
    with pytest.raises(NoAppFoundError):
        import_app('test_apps.invalid_app')
