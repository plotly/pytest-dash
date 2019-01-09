import pytest
from ruamel import yaml


def pytest_collect_file(parent, path):
    if path.ext == ".yml" and path.basename.startswith("test"):
        return DashBehaviorTestFile(path, parent)


class DashBehaviorTestFile(pytest.File):
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

                yield DashBehaviorTestItem(
                    behavior_name, self, behavior, **test[behavior_name]
                )


class DashBehaviorTestItem(pytest.Item):
    def __init__(self, name, parent, spec, **kwargs):
        super(DashBehaviorTestItem, self).__init__(name, parent)
        self.spec = spec
        self.parameters = kwargs

    def runtest(self):
        print(self.proper_name)
        print(self.spec)

    def reportinfo(self):
        return self.fspath, 0, "usecase: %s" % self.proper_name

    @property
    def proper_name(self):
        if self.parameters:
            return self.name + '-' + '-'.join(
                '[{}={}]'.format(k, v)
                for k, v
                in self.parameters.items()
            )
        return self.name
