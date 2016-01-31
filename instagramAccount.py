import sys, json

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
	def uploadNewImage(self):
		# will get a fresh image to upload and upload it using py + php
		raise NotImplementedError
	def makeSpamComment(self):
		# will use arguments to have php comment on something relevant
		raise NotImplementedError
	def makeSpamLike(self):
		# will use php to like a relevant picture
		raise NotImplementedError

class InstagramAccountCollection:
	accounts = []
	def __init__(self):
		pass
	def load_accounts(self, database_file):
		db = open(database_file, 'r')
		raw_contents = db.read()
		db.close()
		json_obj = self._byteify(json.loads(raw_contents))
		
		# removes meaningless '' from beginning
		for _, obj in json_obj.iteritems():
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
		raise NotImplementedError
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