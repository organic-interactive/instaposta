from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display # pip install pyvirtualdisplay 
#									   pip install pyscreenshot
from selenium import webdriver # TODO: probably unneccessary
import time
import urllib, re
from PIL import Image
import cStringIO

class ImageGetter:
	save_directory = ''
	uploaded_ids = []
	img_id = ''
	description = ''
	filetype = ''
	scrape_site = ''
	def __init__(self, uploaded_ids, scrape_site):
		self.save_directory = "img/"
		self.filetype = ".jpg"
		self.uploaded_ids = uploaded_ids
		self.scrape_site = scrape_site
	def get_image(self):
		## Uses supplied scrape site to find new pictures
		url = self.scrape_site
		# virtual display for headless runs
		display = Display(visible=0, size=(800, 600))
		display.start()

		with closing(Firefox()) as browser:
			browser.get(url)
			time.sleep(5) # TODO: fix with something less static, but still
			# multipurpose considering scrape_site as a db var
			imgs = browser.find_elements_by_tag_name('img')
			# TODO: fix this temporary workaround that prevents ad server data
			# from reaching the image checks
			no_ad_imgs = [i for i in imgs if 'adsrvr' not in \
				i.get_attribute('src')]
			for img in no_ad_imgs:
				src = img.get_attribute('src')
				alt = img.get_attribute('alt')
				image_id = re.findall("/photo/(.+?)/", src)[0]
				if(self._check_id(image_id) and self._check_ratios(src)):
					self.img_id = image_id
					self.description = alt
					self._save_hd_image()
					break
		display.stop()
		if (self.img_id):
			return
		raise Exception('Failed to find a suitable image: all out or bugged')
	def get_test_image(self):
		## Returns an image from a static URL
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
					self.img_id = image_id
					self.description = alt
					self._save_hd_image()
					break

	def _save_hd_image(self):
		pic_url = "https://500px.com/photo/" + self.img_id + "/" # hd scrape
		regex = "\"image_url\"\:\[(.+?)\]"
		data = re.findall(regex, urllib.urlopen(pic_url).read())[0]
		url2 = data.split(",")[-2][1:-1].replace("\\/", "/")
		img_write = open(self.save_directory + self.img_id + self.filetype, 
			'wb')

		img_write.write(urllib.urlopen(url2).read())
		img_write.close()
	def _check_id(self, image_id):
		if image_id in self.uploaded_ids:
			return False
		return True
	def _check_ratios(self, image_url):
		# print image_url
		f = cStringIO.StringIO(urllib.urlopen(image_url).read())
		image = Image.open(f)

		width, height = image.size
		ratio = width / float(height)
		# source: https://help.instagram.com/1469029763400082
		if(ratio > 0.8 and ratio < 1.91 and width > 5 and height > 5):
			return True
		else:
			print "Unsuitable image"
			print "ratio: %s, width: %s, height: %s" % (ratio, width, height)
		return False
