"""Test custom behaviors"""


def test_custom_behavior(testdir):
    """
    Test a custom value can be added to the parser.

    :param testdir: testdir fixture
    :return:
    """
    testdir.makeconftest(
        '''
        def pytest_add_behaviors(add_behavior):
            @add_behavior('NUMBER "+" NUMBER')
            def add(n1, n2):
                return int(n1) + int(n2)

            @add_behavior('"Write"i variable "in" element', kind='command')
            def write_command(value, element):
                # Same as enter in but user defined.
                element.send_keys(value)
    '''
    )
    testdir.makeini(
        '''
        [pytest]
        webdriver = Chrome
        log_cli=true
        '''
    )
    testdir.makefile(
        '.yml',
        test_additional_behavior='''
        TestAdditionBehavior:
            application:
                path: test_apps.simple_app
            event:
                - 'enter 2 + 2 in #value'
            outcome:
                - '#value.value should be 4'
        TestWriteCommandBehavior:
            application:
                path: test_apps.simple_app
            parameters:
                value:
                    default: printed value
            event:
                - 'write $value in #value'
            outcome:
                - '#value.value should be "printed value"'
        Tests:
            - TestAdditionBehavior
            - TestWriteCommandBehavior
        '''
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(passed=2)
