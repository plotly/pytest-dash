"""Custom hooks for pytest dash"""

# pylint: disable=unused-argument


def pytest_add_behaviors(add_behavior):
    """
    Use this hook to add custom behavior parsing.

    **Example**
    `conftest.py`

    .. code-block:: python

        def pytest_add_behavior(add_behavior):
            @add_behavior('Text to parse')
            def custom_parse_action(params):
                pass

    :param add_behavior: Decorator for a behavior handler function.
    :return:
    """
