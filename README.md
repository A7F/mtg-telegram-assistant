![Python version](https://img.shields.io/badge/Python-v3.6-blue.svg)

## What can this bot do?
Up to now, this bot can:
- get cards via Scryfall
- get card rulings, pricing and legalities
- store DCI numbers for each player
- store MTG:Arena usernames to challenge your friends
- direct linking to [planeswalker points](https://www.wizards.com/magic/planeswalkerpoints) based on your DCI number

## Bot dependencies
This bot runs with:

- [peewee](https://github.com/coleifer/peewee) (a database ORM)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (of course)
- [scrython](https://github.com/NandaScott/Scrython) (python bindings to Scryfall API)
- [emoji](https://github.com/carpedm20/emoji) (because emojis makes messages waay more fancy!)

## Further improvements
- handle FNM subscriptions
- auto sync with your LGS events posted on facebook
- language localisation
- windows app with UI, in case someone doesn't own a server

the following improvements are supposed to be implemented with Flask:

- internal leaderboard to handle tournaments
- event creation
- match tracker for each event

I can't provide any ETA because I'm working on this project during my free time

## Documentation
I'm trying my best to provide in-detailed documentation in the [wiki section](https://github.com/A7F/mtg-telegram-assistant/wiki), along with install instructions, usage description and so on.

### Commands implemented
| command | description | usage |
| ------- | ----------- | ----- |
| start | start the bot or get your telegram ID | `/start` |
| help | commands explainations | `/help` |
| dci | set current user dci number | `/dci` 12345678 |
| name | set current user name | `/name` John |
| arena | set current user MTG:Arena nickname | `/arena` Joy#17 |
| [[card]] | search a card | [[rift bolt]] |
| ((card)) | search card rulings | ((rift bolt)) |