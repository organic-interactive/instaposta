from imagegetter import ImageGetter
from instagramaccount import *

DATABASE_FILENAME = "accounts.json"

if __name__ == "__main__":
	print """
========================
INSTA POSTA 1.0 STARTING
========================"""
	ig_accs = InstagramAccountCollection()
	ig_accs.load_accounts(DATABASE_FILENAME)
	for ig_acc in ig_accs.accounts:
		# find a new image and add it to the account
		ig_acc.upload_new_image()
		# save after each upload to insure crashes don't create image dupes
		ig_accs.save_accounts(DATABASE_FILENAME)
	print "pce nig we out"