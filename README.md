# mastodon-glossary-bot

*Glossary bot for mastodon, inspired from [codeforamerica/glossary-bot](https://github.com/codeforamerica/glossary-bot)*

This bot is still experimental.


## Install

* Create a repo containing a file named `glossary.csv`, like https://github.com/michelbl/RCAUAF
* Clone this repository.
* With python 3 (preferably in a virtualenv), install the dependencies `pip install -r requirements.txt`
* Copy `.env.sample` to `.env` and modify it appropriately.
* Set up the app : ``echo `cat .env | xargs -d'\n'` python scripts/setup_app.py | sh``
* Test the app : ``echo `cat .env | xargs -d'\n'` python mastodon_glossary_bot.py | sh``
* (optional) Deploy like any heroku app. Set up the configuration with ``echo heroku config:set `cat .env | xargs -d'\n'` | sh``


## Contributing

Contributions are welcome! To contribute, fork this repo and submit a PR.


## Licence

AGPL
