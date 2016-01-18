from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib, re
from PIL import Image
import cStringIO

re1='.*?'	# Non-greedy match on filler
re2='\\d+'	# Uninteresting: int
re3='.*?'	# Non-greedy match on filler
re4='(\\d+)'	# Integer Number 1
rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)

# use firefox to get page with javascript generated content
url = "https://500px.com/popular?categories=Nature,Landscapes"
with closing(Firefox()) as browser:
	browser.get(url)
     # button = browser.find_element_by_name('button')
     # button.click()
     # wait for the page to load
     # WebDriverWait(browser, timeout=10).until(
     #     lambda x: x.find_element_by_id('someId_that_must_be_on_new_page'))
	time.sleep(5)
     # store it to string variable
	# page_source = browser.page_source
	imgs = browser.find_elements_by_tag_name('img')
	for img in imgs:
		src = img.get_attribute('src') # https://drscdn.500px.org/photo/136577753/h%3D300/f956545f52d87b193b03e1852798aa23
		alt = img.get_attribute('alt') # Explore by Furstset

		f = cStringIO.StringIO(urllib.urlopen(src).read())
		im = Image.open(f)
		width, height = im.size

		ratio = width / float(height)

		if(ratio > 0.6 and ratio < 1.3 and width > 5 and height > 5):
			print "aww yiss:"
			print(alt + " " + src)
			print (str(width) + " x " + str(height))
			m = rg.search(src)
			if m:
				picID = m.group(1)
				picURL = "https://500px.com/photo/" + picID + "/" # scrape full size pic
				print picURL + "\n"

				regex = "<img src='(.+?)'>"
				url2 = re.findall(regex, urllib.urlopen(picURL).read())[0]
				f = open("pic.jpg", "wb")
				f.write(urllib.urlopen(url2).read())
				f.close()
