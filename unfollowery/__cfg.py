from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from unfollowery import __utils


def get_driver(enable_logging: bool = False):
    """Checks if the current version of chromedriver exists.
    If it doesn't, downloads it.

    Adds chromedriver to the working directory.
    Sets Chromedriver options to work in headless mode.

    Params:
        enable_logging (bool): If True, Selenium and Chromedriver logs
                               will be displayed in terminal

    Returns:
        webdriver.Chrome: Chromedriver object
    """
    drvr_path = __utils.install()

    options = Options()
    options.headless = True

    if not enable_logging:
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=drvr_path,
                              chrome_options=options)

    return driver
