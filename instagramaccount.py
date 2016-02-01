import subprocess, json
from contextlib import closing
from selenium.webdriver import Firefox # pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib, re
from PIL import Image
import cStringIO
from imagegetter import ImageGetter

UPLOADER_SCRIPT_FILENAME = "upload_aux.php"
UPLOAD_SUCCESS = "SUCCESS"

class InstagramAccount:
	username = ''
	password = ''
	email = ''
	access_token = ''
	image_ids = []
	tags = []
	def __init__(self, username, password, email, access_token, image_ids, 
		tags):
		self.username = username
		self.password = password
		self.email = email
		self.access_token = access_token
		self.image_ids = image_ids
		self.tags = tags
	def upload_new_image(self):
		# will get a fresh image to upload and upload it using py + php
		ig = ImageGetter(self.image_ids)
		ig.get_image()
		self._run_uploader(ig)
		# raise NotImplementedError
	def make_spam_comment(self):
		# will use arguments to have php comment on something relevant
		raise NotImplementedError
	def make_spam_like(self):
		# will use php to like a relevant picture
		raise NotImplementedError
	def gen_structure(self):
		structure = {}
		structure["username"] = self.username
		structure["password"] = self.password
		structure["email"] = self.email
		structure["access_token"] = self.access_token
		structure["image_ids"] = self.image_ids
		structure["tags"] = self.tags
		return structure
	def _run_uploader(self, image):
		image_loc = image.save_directory + image.img_id + image.filetype
		if (self._exec_php(UPLOADER_SCRIPT_FILENAME, self.username, self.password,
			image_loc, image.description) == UPLOAD_SUCCESS):
			self.image_ids.append(image.img_id)
			print image.img_id + ": UPLOAD SUCCESS"
		else:
			print "UPLOAD FAILURE"
	def _exec_php(self, script_loc, *args):
		## Executes the given file with the given arguments synchronously
		param1 = ['php', script_loc]
		for arg in args:
			param1.append(arg)
		p = subprocess.Popen(param1, stdout=subprocess.PIPE)
		result = p.communicate()[0]
		print result
		return result

class InstagramAccountCollection:
	accounts = []
	def __init__(self):
		pass
	def load_accounts(self, database_file):
		db = open(database_file, 'r')
		raw_contents = db.read()
		db.close()
		json_obj = self._byteify(json.loads(raw_contents))
		
		for obj in json_obj:
			username = obj["username"]
			password = obj["password"]
			email = obj["email"]
			access_token = obj["access_token"]
			image_ids = obj["image_ids"]
			tags = obj["tags"]
			loaded_account = InstagramAccount(username, password, email, 
				access_token, image_ids, tags)
			self.accounts.append(loaded_account)
	def save_accounts(self, database_file):
		serializable_accs = []
		for account in self.accounts:
			serializable_accs.append(account.gen_structure())
		json_string = json.dumps(serializable_accs)
		db = open(database_file, 'w')
		db.write(json_string)
		db.close()
	def _byteify(self, input):
		## Simple converter from unicode to ascii for json loads out
		if isinstance(input, dict):
			return {self._byteify(key): self._byteify(value)
					for key, value in input.iteritems()}
		elif isinstance(input, list):
			return [self._byteify(element) for element in input]
		elif isinstance(input, unicode):
			return input.encode('utf-8')
		else:
			return input