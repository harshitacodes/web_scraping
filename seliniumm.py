from selenium import webdriver

DRIVER_PATH = '/usr/bin/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('')