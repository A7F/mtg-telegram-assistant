## What can this bot do?
Up to now, this bot can:
- get cards via Scryfall
- get card rulings, pricing and legalities
- store DCI numbers for each player
- store MTG:Arena usernames to challenge your friends

## Bot dependencies
This bot runs with:

- [peewee](https://github.com/coleifer/peewee) (a database ORM)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (of course)
- [scrython](https://github.com/NandaScott/Scrython) (python bindings to Scryfall API)
- [emoji](https://github.com/carpedm20/emoji) (because emojis makes messages waay more fancy!)

### installing dependencies
If you already have python 3.6 and git installed, start from point 4

Step 1: install git 

`sudo apt-get install git`

Step 2: install python 3.6 and aiohttp dependencies

`sudo apt-get install python3.6 build-essential libssl-dev libffi-dev python3-dev -y`

Step 4: clone this repo 

`git clone https://github.com/A7F/mtg-telegram-assistant.git`

Step 5: install bot dependencies with pip

`cd mtg-telegram-assistant/config && pip install -r requirements.txt`

## Quickstart
1. open telegram and generate a token with botfather 
2. edit file config/config.json with your favourite text editor
3. turn off bot privacy setting
4. add the bot to your LGS telegram group
5. turn off bot "can be added to groups" setting
6. start the bot

### Make it fancy
In order to improve user's experience, you may want to set your bot command list via botfather by copy-paste the following:
```
start - start this bot or get your telegram ID
help - how do I use this bot?
dci - set your dci number
name - set your name
arena - set your Arena nickname
```

## Further improvements
- handle FNM subscriptions
- auto sync with your LGS events posted on facebook
- auto fetch DCI planeswalker points
- language localisation
- windows app with UI, in case someone doesn't own a server

the following improvements are supposed to be implemented with Flask:

- internal leaderboard to handle tournaments
- event creation
- match tracker for each event

I can't provide any ETA because I'm working on this project during my free time

## Documentation
I will provide in-detailed documentation in the wiki section, along with usage description and so on.
Because the bot is still a work in progress, implementing docs in such an early stage just makes no sense at all: the code
is still open to changes in almost everything. 

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