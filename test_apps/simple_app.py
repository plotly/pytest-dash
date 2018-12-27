import flask

import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

import dash_html_components as html
import dash_core_components as dcc


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='value', placeholder='my-value'),
    html.Div(['You entered: ', html.Span(id='out')])
])


@app.callback(Output('out', 'children'), [Input('value', 'value')])
def on_value(value):
    if value is None:
        raise PreventUpdate

    # There's an issue with flask and runpy
    # When run with `runpy.run_path`, flask will be None in the methods.
    req = flask.request.headers
    return value
