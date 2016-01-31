from instagram.client import InstagramAPI
from random import randint
import sys
from collections import OrderedDict

client_id = '6c6a851c0fe64dc3a3246d4cf3c70ff8'
client_secret = '289fcf7b2ccd449aaa775f0e9b2f49d3'
access_token = '2535421462.1fb234f.b337ff519e674b50911f55d14fa63838'
client_ip = 'http://localhost'


# auth
client = InstagramAPI(client_id=client_id,
                      client_secret=client_secret,
                      redirect_uri=client_ip)
print(client.get_authorize_login_url(scope=["basic", "follower_list"]))
code = input().strip()
access_token = client.exchange_code_for_access_token(code)[0]
print("asdf: ".format(access_token))

# we are authenticated, let's ask the followed users
client = InstagramAPI(client_secret="BBBB",
                      access_token=access_token)

users = []
followed, next_ = client.user_follows(user_id="self")
users.extend(followed)

while next_:
    followed_more, next_ = client.user_follows(user_id="self", with_next_url=next_)
    users.extend(followed_more)

print("Following {}".format(len(users)))
