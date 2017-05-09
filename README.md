## Install

1. Clone this repository.
2. With python 3 (preferably in a virtualenv), install the dependencies `pip install -r requirements.txt`
3. Copy `.env.sample` to `.env` and modify it appropriately.
4. Set up the app : ``echo `cat .env | xargs -d'\n'` python scripts/setup_app.py | sh``
5. Test the app : ``echo `cat .env | xargs -d'\n'` python mastodon_glossary_bot.py | sh``
6. (optional) Deploy like any heroku app. Set up the configuration with ``echo heroku config:set `cat .env | xargs -d'\n'` | sh``