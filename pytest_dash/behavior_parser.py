"""Custom lark parser and transformer for dash behavior tests."""
import functools
import six

import lark
from selenium.webdriver.support.ui import Select, WebDriverWait

from pytest_dash.utils import (
    wait_for_element_by_id,
    wait_for_element_by_css_selector,
)

_grammar = r'''
start: compare
    | command

// Variable to use from the parameters
?variable: /\$[a-zA-Z0-9_]+/ -> variable

?raw_value: NUMBER
    | ESCAPED_STRING -> escape_string
    | "true"i -> true
    | "false"i -> false
    | ("null"i | "none"i | "nil"i) -> null

?value: raw_value
    | element_prop
    | variable
    %(value)%

?input_value: raw_value
    | variable

// Elements
element_id: /#[a-zA-Z0-9\-_]+/
element_selector: /\{.*\}/
element: element_id | element_selector
element_prop: element ("." NAME)+

// Comparisons
?eq: "should be"i | "eq" | "=="
?lt: "less than"i | "lt"i | "<"
?lte: "less or equal than"i | "lte"i | "<="
?gt: "greater than"i | "gt"i | ">"
?gte: "greater or equal than"i | "gte"i | ">="

?comparison: eq | lt | lte | gt | gte

compare: value comparison value
    | "text in" element eq value -> text_equal
    | element ("." NAME)+ comparison value -> prop_compare
    | "style" value "of" element eq value -> style_compare

%(custom)%

?command: "clear" element -> clear
    | "click" element -> click
    | "enter" value "in" element -> send_value
    | "select by value" input_value element -> select_by_value
    | "select by text" ESCAPED_STRING element -> select_by_text
    | "select by index" NUMBER element -> select_by_index

%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS
%import common.ESCAPED_STRING
%ignore WS
'''


def _compare(left, comparison, right):
    if comparison.data == 'eq':
        return left == right
    if comparison.data == 'lt':
        return left < right
    if comparison.data == 'lte':
        return left <= right
    if comparison.data == 'gt':
        return left > right
    if comparison.data == 'gte':
        return left >= right
    return False


class BehaviorTransformerMeta(type):
    """
    Dynamically create a parser transformer with user defined behaviors
    """

    def __new__(mcs, name, bases, attributes):
        behaviors = attributes.get('_behaviors', {})
        new_attrs = attributes.copy()
        behaviors_grammar = []
        values = []
        comparisons = []
        commands = []

        def wrapper(fun, inline, meta, tree):
            @functools.wraps(fun)
            @lark.v_args(inline=inline, meta=meta, tree=tree)
            # pylint: disable=unused-argument
            def _wrap(self, *args, **kwargs):
                return fun(*args, **kwargs)

            return _wrap

        for key, behavior in behaviors.items():
            new_attrs[key] = wrapper(
                behavior.handler, behavior.inline, behavior.meta, behavior.tree
            )
            behaviors_grammar.append('{}: {}'.format(key, behavior.syntax))
            if behavior.kind == 'value':
                values.append(key)
            elif behavior.kind == 'comparison':
                comparisons.append(key)
            elif behavior.kind == 'commands':
                commands.append(key)

        new_attrs['grammar'] = _grammar.replace(
            '%(custom)%', '\n'.join(behaviors_grammar)
        ).replace(
            '%(value)%',
            '| ' + '| '.join(values) if values else '',
        ).replace(
            '%(comparisons)%',
            '| ' + '| '.join(comparisons) if comparisons else '',
        ).replace(
            '%(commands)%',
            '|' + '| '.join(commands) if commands else '',
        )

        return type.__new__(mcs, name, bases, new_attrs)


# noinspection PyMethodMayBeStatic
# pylint: disable=no-self-use, missing-docstring, no-member
@six.add_metaclass(BehaviorTransformerMeta)
@lark.v_args(inline=True)
class BehaviorTransformer(lark.Transformer):
    """Transform and execute behavior commands."""

    def __init__(self, driver, variables=None):
        """
        :param driver: Selenium driver to find elements in the tree
        :type driver: selenium.webdriver.remote.webdriver.WebDriver
        """
        self.driver = driver
        self.variables = variables or {}

    def variable(self, name):
        return self.variables.get(name.lstrip('$'))

    def element_id(self, element_id):
        """
        Find an element by id when found in the tree.

        :param element_id:
        :return:
        """
        return wait_for_element_by_id(self.driver, element_id.replace('#', ''))

    def element_selector(self, selector):
        """
        Find an element by selector when found in the tree.

        :param selector:
        :return:
        """
        return wait_for_element_by_css_selector(
            self.driver,
            selector.lstrip('{').rstrip('}')
        )

    def element(self, identifier):
        # Just need to return the element that is already found
        # by element_id or element_selector
        return identifier

    def element_prop(self, element, prop):
        return element.get_property(prop)

    def compare(self, left, comparison, right):
        assert _compare(left, comparison, right)

    def clear(self, element):
        element.clear()

    def click(self, element):
        element.click()

    def send_value(self, value, element):
        element.send_keys(value)

    def select_by_value(self, value, element):
        select = Select(element)
        select.select_by_value(value)

    def select_by_text(self, text, element):
        select = Select(element)
        select.select_by_visible_text(text)

    def select_by_index(self, index, element):
        select = Select(element)
        select.select_by_index(index)

    def escape_string(self, escaped):
        return escaped.strip('"')

    def text_equal(self, element, _, value):
        # We have the element and not the selector so we cannot use the
        # wait_for_text wrapper.
        def _text_equal(_):
            return element.text == value

        WebDriverWait(self.driver, 10).until(_text_equal)

    def prop_compare(self, element, prop, comparison, value):
        def _prop_compare(_):
            prop_value = element.get_property(prop)
            return _compare(prop_value, comparison, value)

        WebDriverWait(self.driver, 10).until(_prop_compare)

    def style_compare(self, style, element, _, value):
        def _style_compare(_):
            style_value = element.value_of_css_property(style)
            return style_value == value

        WebDriverWait(self.driver, 10).until(_style_compare)


def parser_factory(driver, variables=None, behaviors=None):
    """
    Create a Lark parser with a BehaviorTransformer with the provided
    selenium driver to find the elements.

    :param driver: Selenium driver to use when parsing elements.
    :param variables:
    :return:
    """

    class NewBehaviorTransformer(BehaviorTransformer):
        _behaviors = behaviors or {}

    # pylint: disable=no-member
    return lark.Lark(
        NewBehaviorTransformer.grammar,
        parser='lalr',
        transformer=NewBehaviorTransformer(driver, variables)
    )
