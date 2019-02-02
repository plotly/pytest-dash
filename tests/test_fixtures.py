# pylint: disable=redefined-outer-name, missing-docstring
try:
    from queue import Queue
except ImportError:
    # noinspection PyUnresolvedReferences
    from Queue import Queue

import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_html_components as html

# pylint: disable=unused-import
from pytest_dash.utils import \
    wait_for_text_to_equal, wait_for_element_by_css_selector
from pytest_dash.application_runners import import_app


def test_dash_threaded(dash_threaded):
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.Button('click me', id='clicker'),
        html.Div(id='output')
    ])

    call_count = Queue()

    @app.callback(Output('output', 'children'), [Input('clicker', 'n_clicks')])
    def on_click(n_clicks):
        call_count.put(1)
        if n_clicks is None:
            raise PreventUpdate

        return n_clicks

    dash_threaded(app, port=8090)
    assert 'http://localhost:8090' in dash_threaded.driver.current_url

    clicker = wait_for_element_by_css_selector(
        dash_threaded.driver, '#clicker'
    )

    for i in range(6):
        clicker.click()
        wait_for_text_to_equal(dash_threaded.driver, '#output', str(i + 1))

    assert call_count.qsize() == 7


def test_imported_app(dash_threaded):
    app = import_app('test_apps.simple_app')
    dash_threaded(app)

    driver = dash_threaded.driver

    value_input = driver.find_element_by_id('value')
    value_input.clear()
    value_input.send_keys('Hello imported dash')

    wait_for_text_to_equal(driver, '#out', 'Hello imported dash')


def test_subprocess(dash_subprocess):
    dash_subprocess('test_apps.simple_app', port=8080)
    driver = dash_subprocess.driver
    assert 'http://localhost:8080' in driver.current_url

    value_input = driver.find_element_by_id('value')
    value_input.clear()
    value_input.send_keys('Hello dash subprocess')

    wait_for_text_to_equal(driver, '#out', 'Hello dash subprocess')
