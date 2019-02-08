*****
Usage
*****

Install
=======

Install with pip:

``pip install -U pytest-dash``

Write integration tests
=======================

``pytest-dash`` provides fixtures and helper functions
to write `Dash <https://github.com/plotly/dash>`_ integration tests.

To start a Dash instance, you can use a ``dash_threaded`` or
``dash_subprocess`` fixture.

The fixture will start the server when called and wait until the application
has been loaded by the browser. The server will be automatically closed in
the test teardown.

.. include:: ./examples/dash_threaded.rst

.. include:: ./examples/dash_subprocess.rst

.. seealso::

    :Fixtures:

        dash_threaded :py:func:`~.plugin.dash_threaded`

        dash_subprocess :py:func:`~.plugin.dash_subprocess`

Helpers
-------

Importing applications
^^^^^^^^^^^^^^^^^^^^^^

Import existing Dash applications from a file with
:py:func:`~.application_runners.import_app`.
The application must be named app.

:Example:

.. code-block:: python

    from pytest_dash.application_runners import import_app

    def test_application(dash_threaded):
        app = import_app('my_app')
        ...

Selenium wait for wrappers
^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:mod:`~.wait_for` module is especially useful if you need to interact
with elements or props that are only loaded after a callback as there
might be a delay between when the callback is handled
and returned to the frontend.

Available wrappers:

- :py:func:`~.wait_for.wait_for_element_by_css_selector`
- :py:func:`~.wait_for.wait_for_elements_by_css_selector`
- :py:func:`~.wait_for.wait_for_element_by_xpath`
- :py:func:`~.wait_for.wait_for_elements_by_xpath`
- :py:func:`~.wait_for.wait_for_element_by_id`
- :py:func:`~.wait_for.wait_for_text_to_equal`
- :py:func:`~.wait_for.wait_for_style_to_equal`
- :py:func:`~.wait_for.wait_for_property_to_equal`

Write declarative scenario tests
================================

Pytest-dash include a declarative way to generate tests in a yaml format.
When pytest finds yaml files prefixed with ``test_`` in a directory, it will
generate tests from a ``Tests`` object.

Schema
------

A yaml test file contains scenario definitions and a list of parametrized
of scenarios to execute.

Globals
^^^^^^^

:application:

    Global default application to use in the tests if no option supplied.

:Tests:

    List of scenario to generate tests for. Test item props are used as
    parameter.

Scenario object
^^^^^^^^^^^^^^^

:parameters:

    Object where the keys will be used to create a variable dictionary to
    use in behavior commands. Use a parameter in commands by prefixing the key
    with ``$``, (eg: ``$value``).

:application:

    :path: Dot notation path to the application file.
    :options:
        :port: The port used by the application.

    :event:

        List of actions to execute.

    :outcome:

        List of expected result of the scenario event.

.. code-block:: yaml
    :caption: Commented example

    Scenario:           # Key of the test
        parameters:     # Optional values to use in test
            value:
                default: 4
        application:    # The application settings to use in the test
            path: test_apps.simple_app  # Dot notation path to the app file.
            options:    # Application options such as port
                port: 8051
        event:          # List of actions describing what happen.
            - "enter $value in #input"
        outcome:        # The expected result of the event.
            - "text in #output should be $value"

    Tests:              # List of all the scenarios to execute.
        - Scenario      # Runs Scenario with the default parameter.
        - Scenario
            value: 8    # Override the default parameter.

Syntax
------

There is 3 kind of rule for the grammar:

- ``value``, return a value.
- ``command``, execute an action.
- ``comparison``, compare two value.

.. list-table:: Scenario event/outcome syntax
    :header-rows: 1

    *   - Rule
        - Kind
        - Example
        - Description
    *   - element_id
        - value
        - ``#my-element-id``
        - Find a single element by id
    *   - element_selector
        - value
        - ``{#my-element-id > span}``
        - Find a single by selector
    *   - elements_selector
        - value
        - ``*{#my-element-id > span}``
        - Find multiple elements by selector, actions will be executed on all elements
    *   - element_xpath
        - value
        - ``[//*[@id="btn-1"]]``
        - Find a single element by xpath
    *   - elements_xpath
        - value
        - ``*[//div[@id="container"]/span]``
        - Find multiple elements by xpath.
    *   - element_prop
        - value
        - ``#my-input.value``
        - A property of an element to use in comparisons.
    *   - eq
        - comparison
        - ``#my-input.value should be 1``
        - Equality comparison
    *   - lt
        - comparison
        - ``#my-input.value < 3``
        - The value should be less than.
    *   - lte
        - comparison
        - ``#my-input.value <= 3``
        -  The value on the left should be less or equal to.
    *   - gt
        - comparison
        - ``#my-input.value > 3``
        - Value should be greater.
    *   - gte
        - comparison
        - ``#my-input.value >= 3``
        - Greater or equal comparison.
    *   - text_equal
        - comparison
        - ``text in #output should be "Foo bar"``
        - Special comparison for text attribute, it uses the ``wait_for`` api.
    *   - prop_compare
        - comparison
        - ``#output.value should be 3``
        - Property comparison uses the ``wait_for`` api
    *   - style_compare
        - comparison
        - ``style "padding" of #btn should be "3px"``
        - ``wait_for`` comparison for a style attribute of an element.
    *   - clear
        - command
        - ``clear #my-input``
        - Clear the value of an element.
    *   - click
        - command
        - ``click #my-btn``
        - Click on an element, the element must be visible to be clickable.
    *   - send_value
        - command
        - ``enter "Foo bar" in #my-input``
        - Send keyboard input to an element.

.. note:: The syntax can be extended with :ref:`hooks`.

Examples
--------

:Application:

.. literalinclude:: ../test_apps/simple_app.py
    :lines: 2-23
    :caption: simple_app.py
    :name: simple-app

:Test:

.. literalinclude:: ../tests/test_yaml.yml
    :caption: test_simple_callback.yml

.. seealso:: :ref:`component_gallery`

Run tests
=========

Use ``$ pytest tests --webdriver Chrome`` to run all the test

The ``--webdriver`` option is used for choosing the selenium driver to use.
Choose from:

- `Chrome <https://sites.google.com/a/chromium.org/chromedriver/downloads>`_
- `Firefox <https://github.com/mozilla/geckodriver/releases>`_
- `Safari <https://webkit.org/blog/6900/webdriver-support-in-safari-10/>`_
- `Edge <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`_
- Opera
- PhantomJS
- Ie
- Remote

.. note::

    The driver must be available on your environment `PATH`.

.. seealso::

    Please refer to https://selenium-python.readthedocs.io/installation.html
    for selenium installation.

Configuration
-------------

The default webdriver for a project can be specified in
`pytest.ini <https://docs.pytest.org/en/latest/customize.html#adding-default-options>`_
instead of having to enter it on the command line every time you run a test.

:Example: ``./pytest.ini``

.. code-block:: ini

    [pytest]
    webdriver = Chrome

.. _hooks:

Hooks
-----

The scenario event/outcome syntax can be extended with
the :py:func:`~.new_hooks.pytest_add_behaviors` hook.

``add_behavior`` is a decorator with the following keywords arguments:

- ``syntax`` The syntax to match, it will be available under the name of the function in the parser.
- ``kind``
   - ``value`` default, A value can be used in commands and comparisons.
   - ``command``, Complete custom line parsing.
   - ``comparison``, A comparison should ``assert`` something inside the function.
- ``inline/tree/meta`` Only one can to be set to true, default is inline, decorate the function with ``lark.v_args(inline=inline, tree=tree, meta=meta)``, `lark.v_args docs <https://lark-parser.readthedocs.io/en/latest/classes/#v_args>`_.


:Example: ``tests/conftest.py``

.. code-block:: python

    def pytest_add_behaviors(add_behavior):
        @add_behavior('"eval("/.*/")"')
        def evaluate(command):
            return eval(command)


.. seealso::

    Lark grammar reference https://lark-parser.readthedocs.io/en/latest/grammar/
