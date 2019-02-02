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
    html.Div(id='radio-items-output'),
    html.Button('change-style', id='change-style'),
    html.Div(
        'Style changer',
        id='style-output',
        style={'backgroundColor': 'rgba(255, 0, 0, 1)'}
    ),
    html.Div([
        html.Button('btn-1', id='btn-1'),
        html.Button('btn-2', id='btn-2'),
        html.Button('btn-3', id='btn-3'),
    ], id='multi-elements-click'),
    html.Div(id='multi-elements-outputs')
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


@app.callback(
    Output('style-output', 'style'), [Input('change-style', 'n_clicks')]
)
def on_style_change(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    return {'backgroundColor': 'rgba(0, 0, 255, 1)'}


@app.callback(
    Output('multi-elements-outputs', 'children'),
    [Input('btn-{}'.format(x), 'n_clicks') for x in range(1, 4)],
)
def on_multi_click(n1, n2, n3):
    return [html.Span(x) for x in [n1, n2, n3] if x]


if __name__ == '__main__':
    app.run_server(
        debug=True,
        port=9150,
        dev_tools_silence_routes_logging=False,
        dev_tools_hot_reload=False
    )
