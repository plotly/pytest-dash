def test_custom_behavior(testdir):
    testdir.makeconftest(
        '''
        pytest_plugins = ['pytest_dash.plugin']
        
        def pytest_add_behaviors(add_behavior):
            @add_behavior('NUMBER "+" NUMBER')
            def add(n1, n2):
                return int(n1) + int(n2)
    '''
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
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
