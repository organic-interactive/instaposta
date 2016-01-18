import urllib, re

regex = "<img src='(.+?)'>"
url = "https://500px.com/photo/95908145/getting-out-by-kent-mearig?ctx_page=1&from=search&ctx_type=photos&ctx_sort=pulse&ctx_q=adventure"
url2 = re.findall(regex, urllib.urlopen(url).read())[0]
f = open("testpic.jpg", "wb")
f.write(urllib.urlopen(url2).read())
f.close()