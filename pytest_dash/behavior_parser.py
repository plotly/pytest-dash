import lark

from selenium.webdriver.support.ui import Select


from pytest_dash.utils import (
    wait_for_element_by_id,
    wait_for_element_by_css_selector,
)


_grammar = r'''
start: compare
    | command

// Variable to use from the parameters
?variable: /\$[a-zA-Z0-9_]+/

?raw_value: NUMBER
    | ESCAPED_STRING -> escape_string
    | "true"i -> true
    | "false"i -> false
    | ("null"i | "none"i | "nil"i) -> null

?value: raw_value
    | element_prop

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

?command: "clear" element -> clear
    | "click" element -> click
    | "enter" input_value "in" element -> send_value
    | "select by value" input_value element -> select_by_value
    | "select by text" ESCAPED_STRING element -> select_by_text
    | "select by index" NUMBER element -> select_by_index

%import common.CNAME -> NAME
%import common.NUMBER
%import common.WS
%import common.ESCAPED_STRING
%ignore WS
'''


# noinspection PyMethodMayBeStatic
@lark.v_args(inline=True)
class BehaviorTransformer(lark.Transformer):
    """Transform and execute behavior commands."""

    def __init__(self, driver):
        """
        :param driver: Selenium driver to find elements in the tree
        :type driver: selenium.webdriver.remote.webdriver.WebDriver
        """
        self.driver = driver

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
        return wait_for_element_by_css_selector(self.driver, selector)

    def element(self, identifier):
        # Just need to return the element that is already found
        # by element_id or element_selector
        return identifier

    def element_prop(self, element, prop):
        return element.get_property(prop)

    def compare(self, v1, comparison, v2):
        if comparison.data == 'eq':
            assert v1 == v2
        elif comparison.data == 'lt':
            assert v1 < v2
        elif comparison.data == 'lte':
            assert v1 <= v2
        elif comparison.data == 'gt':
            assert v1 > v2
        elif comparison.data == 'gte':
            assert v1 >= v2

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

    def escape_string(self, s):
        return s.strip('"')


def parser_factory(driver):
    """
    Create a Lark parser with a BehaviorTransformer with the provided
    selenium driver to find the elements.

    :param driver:
    :return:
    """
    return lark.Lark(
        _grammar,
        parser='lalr',
        transformer=BehaviorTransformer(driver)
    )
