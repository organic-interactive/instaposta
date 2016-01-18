import urllib, re

search_url = "https://500px.com/popular?categories=Nature,Landscapes"
data = urllib.urlopen(search_url).read()
f = open("stuff.html", "w")
f.write(data)
f.close()
