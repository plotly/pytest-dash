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

    return value
