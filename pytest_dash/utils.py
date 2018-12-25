import runpy

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import By

from pytest_dash.errors import NoAppFoundError


def _wait_for(driver, condition, timeout=10):
    return WebDriverWait(driver, timeout).until(
        condition
    )


def wait_for_element_by_css_selector(driver, selector, timeout=10):
    return _wait_for(
        driver, EC.presence_of_element_located((By.CSS_SELECTOR, selector)),
        timeout=timeout
    )


def wait_for_text_to_equal(driver, selector, text, timeout=10):
    """

    :param driver:
    :type driver: selenium.webdriver.remote.webdriver.WebDriver
    :param selector:
    :param text:
    :param timeout:
    :return:
    """
    def condition(d):
        return text == d.find_element_by_css_selector(selector).text

    _wait_for(
        driver, condition,
        timeout=timeout
    )
    assert text == driver.find_element_by_css_selector(selector).text


def import_app(app_file):
    try:
        app_module = runpy.run_module(app_file)
        app = app_module['app']
    except KeyError:
        raise NoAppFoundError(
            'No dash `app` instance was found in {}'.format(app_file)
        )
    return app
