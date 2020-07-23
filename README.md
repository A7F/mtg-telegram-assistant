![Python version](https://img.shields.io/badge/Python-v3.8-blue.svg)

## What can this bot do?
Up to now, this bot can:
- get cards via Scryfall
- get card rulings, pricing and legalities
- store DCI numbers for each player
- store MTG:Arena usernames to challenge your friends
- read rss feeds from a custom list of websites and post news on your group or even a channel connected to your discussion group
- check mtg arena server [status page](https://magicthegatheringarena.statuspage.io/)
- direct link to [banned and restricted](https://magic.wizards.com/game-info/gameplay/rules-and-formats/banned-restricted) official page
- check [which expansions are in standard and which are rotating](https://whatsinstandard.com)
- send a message with all the links to all your community socials

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
- requests and beautifulsoup4 (to fetch data from mtga server status website)

However you don't have to install all of them manually because I put everything in the requirements file! Visit the wiki if you don't know how to use it ;)
## Further improvements
- handle FNM codes automagically
- auto sync with your LGS events posted on facebook
- language localisation

I can't provide any ETA because I'm working on this project during my free time

## Documentation
I'm trying my best to provide in-detailed documentation in the [wiki section](https://github.com/A7F/mtg-telegram-assistant/wiki), along with install instructions, usage description and so on.
