from mwt import MWT
import strings, datetime
from emoji import emojize
import requests
from config import rotation, headers, config
import logging
import json
import tables
import datetime

logger = logging.getLogger(__name__)
CACHED_FRIENDLIST = [{"TTL": datetime.datetime(2011, 3, 2), "LIST": ""}]
CACHED_LEGALITIES = {}


@MWT(timeout=60*15)
def build_banlist():
    url = "https://magic.wizards.com/game-info/gameplay/rules-and-formats/banned-restricted"
    text = '[{}]({})'.format(strings.Global.format_banlist,url)
    return text


@MWT(timeout=60*30)
def build_rotationlist():
    resp = requests.get(url=rotation, headers=headers)
    data = resp.json()
    standard = []
    standard_stay = []
    standard_leave = []

    if data["deprecated"]:
        logger.warning("warning, api deprecated!!!")
    else:
        for index, expansion in enumerate(data["sets"]):
            enterdate = expansion["enterDate"]["exact"]
            enterdate = datetime.datetime.max if enterdate is None else datetime.datetime.strptime(enterdate,
                                                                                                   '%Y-%m-%dT%H:%M:%S.%f')
            exitdate = expansion["exitDate"]["exact"]
            if exitdate is None:
                est = expansion["exitDate"]["rough"].split(" ")[1]
                exitdate = datetime.datetime.strptime(est, '%Y')
            else:
                exitdate = datetime.datetime.strptime(exitdate, '%Y-%m-%dT%H:%M:%S.%f')

            if enterdate <= datetime.datetime.now() < exitdate:
                standard.append(expansion)
            if exitdate >= datetime.datetime.now():
                standard_stay.append(expansion)
            else:
                standard_leave.append(expansion)

    text = "_will rotate ({}):_\n".format(standard_leave[-4]["exitDate"]["rough"])
    rotate_names = [emojize(":arrows_counterclockwise: " + exp["name"], use_aliases=True) for exp in
                    standard_leave[-4:]]
    stay_names = [emojize(":left_right_arrow: " + exp["name"], use_aliases=True) for exp in standard_stay]
    for names in rotate_names:
        text += names + "\n"
    text += "\n"
    text += "_will stay ({}):_\n".format(standard_stay[0]["exitDate"]["rough"])
    for names in stay_names:
        text += names + "\n"
    return text


# Returns a list of admin IDs for a given chat. Results are cached for 15 min.
@MWT(timeout=60*20)
def get_admin_ids(bot, chat_id=None):
    if chat_id is None:
        ids = config["master"]
    else:
        ids = [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
        with open('config/config.json', "r+") as f:
            config["master"] = ids
            json.dump(config, f, indent=4)
    return ids


def build_friendlist(update, context):
    query = tables.User.select().where(tables.User.arena.is_null(False))
    text = " :dancers: " + strings.Friendlist.friendlist + " :dancers: \n\n"
    timeoffset = datetime.datetime.now() - datetime.timedelta(minutes=10)
    if CACHED_FRIENDLIST[0]["TTL"] < timeoffset:
        logger.warning(strings.Log.new_cache)
        for result in query:
            chat_member = context.bot.getChatMember(chat_id=update.message.chat_id, user_id=result.user_id)
            user = chat_member.user
            if user is None:
                result.delete()
            else:
                if user.username:
                    text += "<a href=\"t.me/{}\">{}</a> - {}\n".format(user.username, result.name, result.arena)
                else:
                    text += "{} - {}\n".format(result.name, result.arena)
        CACHED_FRIENDLIST[0]["LIST"] = text
        CACHED_FRIENDLIST[0]["TTL"] = datetime.datetime.now()
    else:
        logger.warning(strings.Log.cached)
        text = CACHED_FRIENDLIST[0]["LIST"]
    return text
