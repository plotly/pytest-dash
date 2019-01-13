"""Experimental behavioral test api for dash apps."""
import pytest
from ruamel import yaml

from pytest_dash.application_runners import DashSubprocess


# pylint: disable=inconsistent-return-statements, missing-docstring
def pytest_collect_file(parent, path):
    if path.ext == ".yml" and path.basename.startswith("test"):
        return DashBehaviorTestFile(path, parent)


class DashBehaviorTestFile(pytest.File):
    """A yaml test file definition"""

    def collect(self):
        raw = yaml.safe_load(self.fspath.open())
        tests = raw.pop('Tests')
        if not tests:
            raise Exception('No tests definition for the file in')

        for test in tests:
            if isinstance(test, str):
                yield DashBehaviorTestItem(test, self, raw.get(test))
            else:
                behavior_name = list(test.keys())[0]
                behavior = raw.get(behavior_name)
                kwargs = test[behavior_name]
                test_name = behavior_name + '-' + '-'.join(
                    '[{}={}]'.format(k, v) for k, v in kwargs.items()
                )

                yield DashBehaviorTestItem(
                    test_name, self, behavior, **kwargs
                )


class DashBehaviorTestItem(pytest.Item):
    """A single test of a test file."""

    def __init__(self, name, parent, spec, **kwargs):
        super(DashBehaviorTestItem, self).__init__(name, parent)
        self.spec = spec
        self.parameters = kwargs

    # pylint: disable=missing-docstring
    def runtest(self):
        print(self.spec)

    # pylint: disable=missing-docstring
    def reportinfo(self):
        return self.fspath, 0, "usecase: %s" % self.name
