## What can this bot do?
- get cards and pricing via scryfall
- get card rulings and legalities
- stores DCI numbers for each player
- stores MTG:Arena username to challenge your friends

## Dependencies
This bot runs with:

- peewee (a database ORM)
- python-telegram-bot (of course)
- scrython (python bindings to Scryfall API)
- emoji (because emojis makes messages waay more fancy!)

### installing dependencies
If you already have python 3.6 and git installed, start from point 3

Step 1: install git 

`sudo apt-get install git`

Step 2: install python 3.6

`sudo apt-get install python3.6 -y`

Step 3: also install these packages:

`sudo apt-get install build-essential libssl-dev libffi-dev`

Step 4: clone this repo 

`git clone https://github.com/A7F/mtg-telegram-assistant.git`

Step 5: install python dependencies with pip

`cd config && pip install -r requirements.txt`

## Quickstart
5. open telegram and generate a token with botfather 
6. edit file config/config.json with your favourite text editor
7. turn off bot privacy setting
8. add the bot to your LGS telegram group
9. turn off bot "can be added to groups" setting
10. start the bot

## Further improvements
- handle FNM subscriptions
- auto sync with your LGS events posted on facebook
- auto fetch DCI planeswalker points
- language localisation

the following improvements are supposed to be implemented by integrating a Flask server in the bot:

- internal leaderboard to handle tournaments
- event creation
- match tracker for every single event

## Documentation
I will provide in-detailed documentation in the wiki section, along with usage description and so on.
Because the bot is still a work in progress, implementing docs in such an early stage just makes no sense at all: the code
is still open to changes in almost everything. 
