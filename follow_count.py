import urllib, re, time

def get_follower_count(username):
	regex = "\"followed_by\":\{\"count\":(.+?)\}"
	url = "https://www.instagram.com/"
	url_final = url + username
	return int(re.findall(regex, urllib.urlopen(url_final).read())[0].replace(",",""))

if __name__ == "__main__":
	username = "amazing_outside"
	wait_time = 60
	while True:
		print get_follower_count(username)
		time.sleep(wait_time)