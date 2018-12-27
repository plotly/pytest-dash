try:
    from queue import Queue
except ImportError:
    # noinspection PyUnresolvedReferences
    from Queue import Queue

import pytest
import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_html_components as html

from pytest_dash.fixtures import dash_threaded, dash_subprocess
from pytest_dash.errors import NoAppFoundError, DashAppLoadingError
from pytest_dash.utils import \
    wait_for_text_to_equal, wait_for_element_by_css_selector, import_app


def test_dash_threaded(dash_threaded, selenium):
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.Button('click me', id='clicker'),
        html.Div(id='output')
    ])

    call_count = Queue()

    @app.callback(Output('output', 'children'),
                  [Input('clicker', 'n_clicks')])
    def on_click(n_clicks):
        call_count.put(1)
        if n_clicks is None:
            raise PreventUpdate

        return n_clicks

    dash_threaded(app, port=8090)
    assert 'http://localhost:8090' in selenium.current_url

    clicker = wait_for_element_by_css_selector(selenium, '#clicker')

    for i in range(6):
        clicker.click()
        wait_for_text_to_equal(selenium, '#output', str(i + 1))

    assert call_count.qsize() == 7


def test_invalid_start_raises(dash_threaded):
    app = dash.Dash(__name__)

    # Start the server without setting the layout.
    with pytest.raises(DashAppLoadingError):
        dash_threaded(app, start_timeout=1)


@pytest.mark.skipif('os.environ.get("CIRCLECI")',
                    reason='Bugged because of #15')
def test_imported_app(dash_threaded, selenium):
    app = import_app('test_apps.simple_app')
    dash_threaded(app)

    value_input = selenium.find_element_by_id('value')
    value_input.clear()
    value_input.send_keys('Hello imported dash')

    wait_for_text_to_equal(selenium, '#out', 'Hello imported dash')


def test_no_app_found():
    error = None

    try:
        app = import_app('test_apps.bad')
    except NoAppFoundError as e:
        error = e

    assert isinstance(error, NoAppFoundError)


@pytest.mark.skipif('os.environ.get("CIRCLECI")',
                    reason='Not working on circle.')
def test_subprocess(dash_subprocess, selenium):
    dash_subprocess('test_apps.simple_app', port=8080)
    assert 'http://localhost:8080' in selenium.current_url

    value_input = selenium.find_element_by_id('value')
    value_input.clear()
    value_input.send_keys('Hello dash subprocess')

    wait_for_text_to_equal(selenium, '#out', 'Hello dash subprocess')
