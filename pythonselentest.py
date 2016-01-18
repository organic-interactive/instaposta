from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
import time

# use firefox to get page with javascript generated content
url = "https://500px.com/search?q=adventure&type=photos&sort=pulse"
with closing(Firefox()) as browser:
	browser.get(url)
     # button = browser.find_element_by_name('button')
     # button.click()
     # wait for the page to load
     # WebDriverWait(browser, timeout=10).until(
     #     lambda x: x.find_element_by_id('someId_that_must_be_on_new_page'))
	time.sleep(5)
     # store it to string variable
	page_source = browser.page_source
if "kent" in page_source:
	print "great success"
else:
	print "no dice"
# f = open("html.html", "w")
# f.write(page_source)
# f.close()