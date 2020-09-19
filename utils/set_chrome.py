from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
The following code will set Google Chrome options to work in headless mode.
Headless mode - Running browser/driver in background without popping up.
"""
options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path = 'utils\chromedriver.exe', chrome_options = options)

"""
Here's the other way of doing so:
    options = Options()
    options.add_argument("--headless") #Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') #Bypass OS security model.
    options.add_argument('--disable-gpu')  #Applicable to windows os only.
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options = options, executable_path = chromedriver.exe)
"""