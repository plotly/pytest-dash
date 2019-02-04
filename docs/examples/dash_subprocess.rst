`dash_subprocess` example
-------------------------

Start the server in subprocess with ``waitress-serve``.
Kill the process in teardown.

.. code-block:: python

    from pytest_dash.wait_for import wait_for_text_to_equal

    def test_subprocess(dash_subprocess):
        driver = dash_subprocess.driver
        dash_subprocess('test_apps.simple_app')

        value_input = driver.find_element_by_id('value')
        value_input.clear()
        value_input.send_keys('Hello dash subprocess')

        wait_for_text_to_equal(driver, '#out', 'Hello dash subprocess')

.. note:: This fixture is slower than threaded due to the process spawning.
