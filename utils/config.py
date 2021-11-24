from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import os


"""
1. Check if the current version of chromedriver exists.
   If it doesn't, download it automatically.
   Then add chromedriver to this directory.

2. Set Chromedriver options to work in headless mode.

* Headless mode - Running browser/driver in background without popping up.
"""
cur_dir = os.path.join(os.path.abspath(os.path.curdir), 'utils')
drvr_path = chromedriver_autoinstaller.install(path=cur_dir)

options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path=drvr_path,
                          chrome_options=options)

# Set sleep time as you wish
sleep_time = 5
