# pytest-dash

[Pytest][2] fixtures for [dash][1].

[![CircleCI](https://circleci.com/gh/T4rk1n/pytest-dash.svg?style=svg)](https://circleci.com/gh/T4rk1n/pytest-dash)
[![Documentation Status](https://readthedocs.org/projects/pytest-dash/badge/?version=latest)](https://pytest-dash.readthedocs.io/en/latest/?badge=latest)

## Install

`$ pip install pytest-dash`

### Fixtures

#### `dash_threaded`

Start a dash instance in a thread, stop the server in teardown. Use this if
you need to count how many times a callback was fired.

```python
import dash

import dash_html_components as html

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from pytest_dash.utils import wait_for_element_by_css_selector
from pytest_dash.utils import wait_for_text_to_equal

def test_app(dash_threaded, selenium):
    app = dash.Dash(__name__)
    counts = {'clicks': 0}
    
    app.layout = html.Div([
        html.Div('My test layout', id='out'),
        html.Button('click me', id='click-me')
    ])
    
    @app.callback(Output('out', 'children'), [Input('click-me', 'n_clicks')])
    def on_click(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        
        counts['clicks'] += 1
        return 'Clicked: {}'.format(n_clicks)
    
    dash_threaded(app)
    
    btn = wait_for_element_by_css_selector(selenium, '#click-me')
    btn.click()
    
    wait_for_text_to_equal(selenium, '#out', 'Clicked: 1')
    assert counts['clicks'] == 1
```

#### `dash_subprocess`

**experimental**

Start an `app` instance contained in a module with waitress-serve in a
subprocess. Kill the process in teardown.

```python
from pytest_dash.utils import wait_for_text_to_equal

def test_subprocess(dash_subprocess, selenium):
    dash_subprocess('test_apps.simple_app')

    value_input = selenium.find_element_by_id('value')
    value_input.clear()
    value_input.send_keys('Hello dash subprocess')

    wait_for_text_to_equal(selenium, '#out', 'Hello dash subprocess')
```

### Utils

Helper methods.

- `wait_for_element_by_css_selector(driver, selector, timeout=10)`,
- `wait_for_text_to_equal(driver, selector, text, timeout=10)`
- `import_app(app_file)`, Load a file with `runpy`, return the app instance.

## More resources

- [Dash user guide](https://dash.plot.ly/)
- [Pytest][2]
- [Documentation][3]


[1]: https://github.com/plotly/dash
[2]: https://github.com/pytest-dev/pytest
[3]: https://pytest-dash.readthedocs.io/en/latest/
