from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib, re
from PIL import Image
import cStringIO

if False:
	re1='.*?'	# Non-greedy match on filler
	re2='\\d+'	# Uninteresting: int
	re3='.*?'	# Non-greedy match on filler
	re4='(\\d+)'	# Integer Number 1
	rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
	ID_FILE = "uploaded.txt"

	def get_checked_ids():
		f = open(ID_FILE, "r")
		contents = f.read()
		f.close()
		# so that the initial comma that's hacked in doesn't fuck something up
		return remove_white_space(contents)[1:].split(",") 
	def remove_white_space(str):
		return str.replace(" ", "").replace("\t", "").replace("\n", "")

	ids = get_checked_ids()

	def check_ratios(image):
		width, height = image.size
		ratio = width / float(height)
		if(ratio > 0.6 and ratio < 1.3 and width > 5 and height > 5):
			return True
		return False
	def check_id(image_id):
		if image_id in ids:
			return False
		return True
	def add_id(image_id):
		ids.append(image_id)
		f = open(ID_FILE, "a")
		f.write("," + image_id)
		f.close()

	# use firefox to get page with javascript generated content
	url = "https://500px.com/popular?categories=Nature,Landscapes"
	with closing(Firefox()) as browser:
		browser.get(url)
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
			

			if(check_ratios(im)):
				# print "aww yiss:"
				# print(alt + " " + src)
				# print (str(width) + " x " + str(height))
				m = rg.search(src)
				if m:
					picID = m.group(1)
					picURL = "https://500px.com/photo/" + picID + "/" # scrape full size pic
					# print picURL + "\n"

					regex = "<img src='(.+?)'>"
					url2 = re.findall(regex, urllib.urlopen(picURL).read())[0]
					if check_id(picID):
						f = open("pic.jpg", "wb")
						f.write(urllib.urlopen(url2).read())
						f.close()
class ImageGetter:
	save_directory = ''
	uploaded_ids = []
	img_id = ''
	description = ''
	def __init__(self, uploaded_ids):
		self.save_directory = "img/"
		self.uploaded_ids = uploaded_ids
	def get_image(self):
		url = "https://500px.com/popular?categories=Nature,Landscapes"
		with closing(Firefox()) as browser:
			browser.get(url)
			time.sleep(5) # TODO: fix with something less static
			imgs = browser.find_elements_by_tag_name('img')
			for img in imgs:
				src = img.get_attribute('src')
				alt = img.get_attribute('alt')
				image_id = re.findall("/photo/(.+?)/", src)[0]
				if(self._check_id(image_id) and self._check_ratios(src)):
					img_write = open(self.save_directory + image_id + ".jpg", 'wb')
					img_write.write(urllib.urlopen(src).read())
					img_write.close()
					self.img_id = image_id
					self.description = alt
					break

	def _check_id(self, image_id):
		if image_id in self.uploaded_ids:
			return False	
		return True
	def _check_ratios(self, image_url):
		f = cStringIO.StringIO(urllib.urlopen(image_url).read())
		image = Image.open(f)

		width, height = image.size
		ratio = width / float(height)

		if(ratio > 0.6 and ratio < 1.3 and width > 5 and height > 5):
			return True
		return False