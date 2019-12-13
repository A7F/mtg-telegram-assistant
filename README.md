![Python version](https://img.shields.io/badge/Python-v3.6-blue.svg)

## What can this bot do?
Up to now, this bot can:
- get cards via Scryfall
- get card rulings, pricing and legalities
- store DCI numbers for each player
- store MTG:Arena usernames to challenge your friends
- direct linking to [planeswalker points](https://www.wizards.com/magic/planeswalkerpoints) based on your DCI number
- read rss feeds from a custom list of websites

### Some examples...
On the left: a basic card search. On the right, rulings search for card named "austere command"

![pic2](https://image.ibb.co/nnUCSA/photo-2018-11-22-18-16-24.jpg) ![pic1](https://image.ibb.co/eMoHuq/photo-2018-11-22-18-16-34.jpg)  

Player card via inline mode...

![pic3](https://image.ibb.co/f5ZRLV/Inkedphoto-2018-11-22-18-16-38-LI.jpg)

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

the following improvements are supposed to be implemented with Flask, maybe as a companion app:

- internal leaderboard to handle tournaments
- event creation
- match tracker for each event

I can't provide any ETA because I'm working on this project during my free time

## Documentation
I'm trying my best to provide in-detailed documentation in the [wiki section](https://github.com/A7F/mtg-telegram-assistant/wiki), along with install instructions, usage description and so on.
