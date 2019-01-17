# pylint: disable=missing-docstring
import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='input'),
    dcc.Dropdown(
        id='dropdown',
        options=[{
            'label': str(x),
            'value': str(x)
        } for x in range(1, 10)]
    ),
    dcc.RadioItems(
        id='radio-items',
        options=[{
            'label': str(x),
            'value': str(x)
        } for x in range(1, 10)]
    ),
    html.Div(id='input-output'),
    html.Div(id='dropdown-output'),
    html.Div(id='radio-items-output')
])

for i in (
        'input',
        'dropdown',
        'radio-items',
):

    @app.callback(
        Output('{}-output'.format(i), 'children'), [Input(i, 'value')]
    )
    def _wrap(value):
        if value is None:
            raise PreventUpdate

        return str(value)


if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=9150,
        dev_tools_silence_routes_logging=False,
        dev_tools_hot_reload=False
    )
