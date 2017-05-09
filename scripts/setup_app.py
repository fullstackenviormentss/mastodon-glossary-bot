import os

from mastodon import Mastodon


# Register app

creds = Mastodon.create_app(
     'mastodon_glossary_bot',
      to_file = 'clientcred.txt',
      api_base_url=os.environ['API_BASE_URL'],
)

client_id, client_secret = creds
with open('.env', 'a') as f:
    f.write('CLIENT_ID={}\n'.format(client_id))
    f.write('CLIENT_SECRET={}\n'.format(client_secret))


# Log in

mastodon = Mastodon(
    client_id=client_id,
    client_secret=client_secret,
    api_base_url=os.environ['API_BASE_URL'],
)

usercred = mastodon.log_in(
    username=os.environ['BOT_USER_EMAIL'],
    password=os.environ['BOT_USER_PASSWORD'],
)

with open('.env', 'a') as f:
    f.write('ACCESS_TOKEN={}\n'.format(usercred))
