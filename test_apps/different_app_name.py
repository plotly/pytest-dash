# pylint: disable=missing-docstring
import dash
import dash_html_components as html

different = dash.Dash(__name__)
different.layout = html.Div('Different', id='body')
