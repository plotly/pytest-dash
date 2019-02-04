`dash_threaded` example
-----------------------

Start a dash application in a thread, close the server in teardown.

In this example we count the number of times a callback method is called
each time a clicked is called and assert the text output of a callback
by using :py:func:`~.wait_for.wait_for_text_to_equal`.

.. code-block:: python

    import dash
    import dash_html_components as html
    from dash.dependencies import Output, Input

    from pytest_dash import wait_for

    def test_application(dash_threaded):
        # The selenium driver is available on the fixture.
        driver = dash_threaded.driver
        app = dash.Dash(__name__)
        counts = {'clicks': 0}

        app.layout = html.Div([
            html.Div('My test layout', id='out'),
            html.Button('click me', id='click-me')
        ])

        @app.callback(
            Output('out', 'children'),
            [Input('click-me', 'n_clicks')]
        )
        def on_click(n_clicks):
            if n_clicks is None:
                raise PreventUpdate

            counts['clicks'] += 1
            return 'Clicked: {}'.format(n_clicks)

        dash_threaded(app)

        btn = wait_for.wait_for_element_by_css_selector(driver, '#click-me')
        btn.click()

        wait_for.wait_for_text_to_equal(driver, '#out', 'Clicked: 1')
        assert counts['clicks'] == 1
