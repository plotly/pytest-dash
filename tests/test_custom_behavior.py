"""Test custom behaviors"""
import os


def test_custom_behavior(testdir):
    """
    Test a custom value can be added to the parser.

    :param testdir: testdir fixture
    :return:
    """
    cwd = os.getcwd()
    testdir.makeconftest(
        '''
        import os
        os.chdir('{}')
        pytest_plugins = ['pytest_dash.plugin']
        def pytest_add_behaviors(add_behavior):
            @add_behavior('NUMBER "+" NUMBER')
            def add(n1, n2):
                return int(n1) + int(n2)
    '''.format(cwd)
    )
    testdir.makeini('''
    [pytest]
    webdriver = Chrome
    ''')
    testdir.makefile(
        '.yml',
        test_hello_world='''
        TestHelloWorld:
            application:
                path: test_apps.simple_app
            event:
                - 'enter 2 + 2 in #value'
            outcome:
                - '#value.value should be 4'
        Tests:
            - TestHelloWorld
        '''
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=1)
