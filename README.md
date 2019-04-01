# pytest-dash

[Pytest][2] plugin for [Dash][1]. Pytest-dash aims to ease automated testing of dash applications and components.

[![CircleCI](https://circleci.com/gh/plotly/pytest-dash.svg?style=svg)](https://circleci.com/gh/plotly/pytest-dash)
[![Documentation Status](https://readthedocs.org/projects/pytest-dash/badge/?version=latest)](https://pytest-dash.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/T4rk1n/pytest-dash/branch/master/graph/badge.svg)](https://codecov.io/gh/T4rk1n/pytest-dash)

## Install

Install with pip: `$ pip install -U pytest-dash`

## Features

- Fixtures to start [Dash][1] applications and closes them in teardown.
- Declarative behavior test api in a yaml format.
- Selenium wait for wrappers.

## Documentation

For full documentation and examples, please see https://pytest-dash.readthedocs.io/en/latest/usage.html

## Bugs/Suggestions

For any bug, suggestion or request, please open a [GitHub issue](https://github.com/plotly/pytest-dash/issues).

## More resources

- [Dash user guide](https://dash.plot.ly/)
- [Pytest][2]

[1]: https://github.com/plotly/dash
[2]: https://github.com/pytest-dev/pytest
