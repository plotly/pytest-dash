"""Utils methods for pytest-dash such wait_for wrappers and import_app."""
import runpy

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By

from pytest_dash.errors import NoAppFoundError


def _wait_for(driver, condition, timeout=10.0):
    return WebDriverWait(driver, timeout).until(condition)


def _wait_for_element(driver, by, accessor, timeout=10.0):
    return _wait_for(
        driver,
        EC.presence_of_element_located((by, accessor)),
        timeout=timeout
    )


def wait_for_element_by_css_selector(driver, selector, timeout=10.0):
    """
    Wait until a single element is found and return it.
    This variant use the css selector api:
    https://www.w3schools.com/jsref/met_document_queryselector.asp

    :param driver: Selenium driver
    :type driver: selenium.webdriver.remote.webdriver.WebDriver
    :param selector: CSS selector to find.
    :type selector: str
    :param timeout: Maximum time to find the element.
    :type timeout: float
    :return:
    """
    return _wait_for_element(
        driver, By.CSS_SELECTOR, selector, timeout=timeout
    )


def wait_for_element_by_xpath(driver, xpath, timeout=10):
    """
    Wait until a single element is found and return it.
    This variant use xpath to find the element.
    https://www.w3schools.com/xml/xml_xpath.asp

    :param driver: Selenium driver
    :type driver: selenium.webdriver.remote.webdriver.WebDriver
    :param xpath: Xpath query string.
    :type xpath: str
    :param timeout: Maximum time to find the element.
    :type timeout: float
    :return:
    """
    return _wait_for_element(driver, By.XPATH, xpath, timeout=timeout)


def wait_for_element_by_id(driver, _id, timeout=10):
    """
    Wait until a single element is found and return it.
    This variant find by id.

    :param driver: Selenium driver
    :type driver: selenium.webdriver.remote.webdriver.WebDriver
    :param _id: The id of the element to find.
    :param timeout: Maximum time to find the element.
    :type timeout: float
    :return:
    """
    return _wait_for_element(driver, By.ID, _id, timeout=timeout)


def wait_for_text_to_equal(driver, selector, text, timeout=10):
    """
    Wait an element text found by css selector is equal to text.

    :param driver: Selenium driver
    :type driver: selenium.webdriver.remote.webdriver.WebDriver
    :param selector: Selector of the element to assert it's text property.
    :type selector: str
    :param text: Text to equal.
    :type text: str
    :param timeout: Maximum time for the text to equal.
    :type timeout: float
    :return:
    """

    def condition(d):
        return text == d.find_element_by_css_selector(selector).text

    _wait_for(driver, condition, timeout=timeout)


def wait_for_style_to_equal(
        driver, selector, style_attribute, style_assertion, timeout=10
):
    """
    Wait for an element style attribute to equal.

    :param driver: Selenium driver
    :type driver: selenium.webdriver.remote.webdriver.WebDriver
    :param selector: Selector of the element to assert it's style property.
    :type selector: str
    :param style_attribute: The name of the CSS attribute to assert.
    :type style_attribute: str
    :param style_assertion: The value to equal of CSS attribute.
    :type style_assertion: str
    :param timeout: Maximum time.
    :type timeout: float
    :return:
    """

    def condition(d):
        return style_assertion == d.find_element_by_css_selector(selector)\
            .value_of_css_property(style_attribute)

    _wait_for(driver, condition, timeout=timeout)


def wait_for_property_to_equal(
        driver, selector, prop_name, prop_value, timeout=10
):
    """
    Wait for an element property to equal a value.

    :param driver: Selenium driver
    :type driver: selenium.webdriver.remote.webdriver.WebDriver
    :param selector: Selector of the element to assert it's property.
    :type selector: str
    :param prop_name: The name of property.
    :type prop_name: str
    :param prop_value: The value to assert.
    :param timeout: Maximum time.
    :type timeout: float
    :return:
    """

    def condition(d):
        return prop_value == d.find_element_by_css_selector(selector)\
            .get_property(prop_name)

    _wait_for(driver, condition, timeout=timeout)


def import_app(app_file):
    """
    Import a dash application from a module.
    The import path is in dot notation to the module.
    The variable named app will be returned.

    *Example*

        >>> app = import_app('my_app.app')

    Will import the application in module `app` of the package `my_app`.

    :param app_file: Path to the app (dot-separated).
    :type app_file: str
    :raise: pytest_dash.errors.NoAppFoundError
    :return: App from module.
    :rtype: dash.Dash
    """
    try:
        app_module = runpy.run_module(app_file)
        app = app_module['app']
    except KeyError:
        raise NoAppFoundError(
            'No dash `app` instance was found in {}'.format(app_file)
        )
    return app
