class InstagramAccount:
	username = ''
	password = ''
	email = ''
	access_token = ''
	image_ids = []
	tags = []
	def __init__(self, username, password, email, access_token, image_ids, 
		tags):
		this.username = username
		this.password = password
		this.email = email
		this.access_token = access_token
		this.image_ids = image_ids
		this.tags = tags
	def uploadNewImage():
		# will get a fresh image to upload and upload it using py + php
		raise NotImplementedError
	def makeSpamComment():
		# will use arguments to have php comment on something relevant
		raise NotImplementedError
	def makeSpamLike():
		# will use php to like a relevant picture
		raise NotImplementedError