from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from shutil import which

chrome_options = Options()
chrome_options.add_argument("--headless")

# chrome_path = which("chromedriver")

driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
driver.get("https://duckduckgo.com/")

search_input = driver.find_element_by_id("search_form_input_homepage")
# or driver.find_element_by_class_name()
# or driver.find_elements_by_class_name()
# or driver.find_element_by_tag_name()
# or driver.find_elements_by_tag_name()
# or driver.find_element_by_xpath()
# or driver.find_elements_by_xpath()
# or driver.find_element_by_css_selector()
# or driver.find_elements_by_css_selector()
search_input.send_keys("My User Agent")

# search_btn = driver.find_element_by_id("search_button_homepage")
# search_btn.click()
# ---OR---
search_input.send_keys(Keys.ENTER)

print(driver.page_source)

driver.close()