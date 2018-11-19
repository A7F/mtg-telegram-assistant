# some useful links:
# https://python-telegram-bot.org/
# http://docs.peewee-orm.com/en/latest/peewee/quickstart.html
# https://python-telegram-bot.readthedocs.io/en/stable/telegram.user.html#telegram.User

import logging, json, telegram, Tables, scrython, re, asyncio, time, Strings
from telegram import InlineQueryResultArticle, InputTextMessageContent
from mwt import MWT
from functools import wraps
from telegram import ChatAction
from peewee import *
from emoji import emojize
from telegram.ext import Updater, InlineQueryHandler
from telegram.ext import MessageHandler, CommandHandler, Filters


with open('config/config.json', "r+") as f:
    f.seek(0)
    config = json.load(f)

db = SqliteDatabase(config["database"]["path"])
bot = telegram.Bot(token=config["token"])
updater = Updater(token=config["token"])
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
max_cards = 4

try:
    open(config["database"]["path"])
    logging.info(Strings.Log.database_ready)
except FileNotFoundError:
    logging.info(Strings.Log.database_not_found)
    db.create_tables([Tables.User, Tables.Event, Tables.Round])
    logging.log(logging.INFO, Strings.Log.database_ok)
finally:
    db.connect()


# Returns a list of admin IDs for a given chat. Results are cached for 15 min.
@MWT(timeout=60*15)
def get_admin_ids(bot, chat_id=None):
    if chat_id is None:
        ids = config["master"]
    else:
        ids = [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
        with open('config/config.json', "r+") as f:
            config["master"] = ids
            json.dump(config, f, indent=4)
    return ids


def send_action(action):
    """Sends `action` while processing func command."""
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.message.chat_id, action=action)
            func(bot, update, **kwargs)
        return command_func
    return decorator


def start_pvt(bot, update):
    try:
        user = Tables.User.get(Tables.User.user_id == update.message.from_user.id)
        text = Strings.Start.start_pvt
    except DoesNotExist:
        text = Strings.Global.user_not_exist
    finally:
        text += Strings.Start.start_id.format(update.message.from_user.id)
        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)


def start_group(bot, update):
    get_admin_ids(bot, update.message.chat_id)
    try:
        user = Tables.User.get(Tables.User.user_id == update.message.from_user.id)
        bot.send_message(chat_id=update.message.chat_id, text=Strings.Global.user_already_exist)
    except DoesNotExist:
        member = Tables.User.create(user_id=update.message.from_user.id, group=update.message.chat_id,
                                    name=update.message.from_user.first_name)
        bot.send_message(chat_id=update.message.chat_id, text=Strings.Global.welcome, parse_mode=telegram.ParseMode.MARKDOWN)


@send_action(ChatAction.TYPING)
def dci(bot, update):
    args = update.message.text.split(" ")
    if len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text=Strings.Dci.dci_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        dci = args[1]
        try:
            user = Tables.User.get(Tables.User.user_id == update.message.from_user.id)
            user.dci = dci
            user.save()
            bot.send_message(chat_id=update.message.chat_id,
                             text=Strings.Dci.dci_set.format(dci),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            bot.send_message(chat_id=update.message.chat_id,
                             text=Strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@send_action(ChatAction.TYPING)
def name(bot, update):
    args = update.message.text.split(" ")
    if len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text=Strings.Name.name_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        name = args[1]
        try:
            user = Tables.User.get(Tables.User.user_id == update.message.from_user.id)
            user.name = name
            user.save()
            bot.send_message(chat_id=update.message.chat_id,
                             text=Strings.Name.name_set.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            bot.send_message(chat_id=update.message.chat_id,
                             text=Strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@send_action(ChatAction.TYPING)
def arena(bot, update):
    args = update.message.text.split(" ")
    if len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text=Strings.Arena.arena_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        arena = args[1]
        try:
            user = Tables.User.get(Tables.User.user_id == update.message.from_user.id)
            user.arena = arena
            user.save()
            bot.send_message(chat_id=update.message.chat_id,
                             text=Strings.Arena.arena_set.format(arena),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            bot.send_message(chat_id=update.message.chat_id,
                             text=Strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@send_action(ChatAction.UPLOAD_PHOTO)
def cards(bot, update):
    match = re.findall(r'\[\[(.*?)\]\]', update.message.text)
    asyncio.set_event_loop(asyncio.new_event_loop())
    for index, name in enumerate(match):
        if index > max_cards:
            break
        try:
            card = scrython.cards.Named(fuzzy=name)
        except Exception:
            bot.send_message(chat_id=update.message.chat_id,
                             text=Strings.Card.card_not_found.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
            continue
        not_legal = [k for k, v in card.legalities().items() if v == "not_legal"]
        legal_in = ""
        if len(not_legal) == 0:
            legal_in = Strings.Card.card_legal
        else:
            for v in not_legal:
                legal_in += v + " "
        try:
            eur = card.currency(mode="eur") + "€"
        except KeyError:
            eur = Strings.Card.card_unavailable
        try:
            usd = card.currency(mode="usd") + "$"
        except KeyError:
            usd = Strings.Card.card_unavailable

        usd_link = card.purchase_uris().get("tcgplayer")
        eur_link = card.purchase_uris().get("magiccardmarket")
        if eur_link is None:
            eur_link = "www.mtgcardmarket.com"
        if usd_link is None:
            usd_link = "www.tcgplayer.com"

        img_caption = emojize(":moneybag: [" + eur + "]" + "(" + eur_link + ")" + " | "
                              + "[" + usd + "]" + "(" + usd_link + ")" + "\n"
                              + ":no_entry: "+legal_in, use_aliases=True)
        bot.send_photo(chat_id=update.message.chat_id, photo=card.image_uris(0, image_type="normal"),
                       caption=img_caption, parse_mode=telegram.ParseMode.MARKDOWN,
                       reply_to_message_id=update.message.message_id)
        time.sleep(0.04)


@send_action(ChatAction.TYPING)
def rulings(bot, update):
    match = re.findall(r'\(\((.*?)\)\)', update.message.text)
    asyncio.set_event_loop(asyncio.new_event_loop())
    for index, name in enumerate(match):
        if index > max_cards:
            break
        card = scrython.cards.Named(fuzzy=name)
        try:
            card = scrython.cards.Named(fuzzy=name)
        except Exception:
            bot.send_message(chat_id=update.message.chat_id,
                             text=Strings.Card.card_not_found.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
            continue
        rule = scrython.rulings.Id(id=card.id())
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        message = ""
        if rule.data_length() == 0:
            message = Strings.Card.card_ruling_unavailable
        else:
            for index, rule_text in enumerate(rule.data()):
                message += (str(index + 1) + ". " + rule.data(index=index, key="comment") + "\n\n")
        bot.send_message(chat_id=update.message.chat_id, text=message, reply_to_message_id=update.message.message_id)
        time.sleep(0.07)


@send_action(ChatAction.TYPING)
def help(bot, update):
    if update.message.from_user.id in get_admin_ids(bot):
        text = Strings.Help.admin_help
    else:
        text = Strings.Help.user_help
    bot.send_message(chat_id=update.message.chat_id,
                     text=emojize(text, use_aliases=True),
                     parse_mode=telegram.ParseMode.MARKDOWN)


def inline(bot, update):
    query = update.inline_query.query
    try:
        user = Tables.User.get(Tables.User.user_id == update.inline_query.from_user.id)
        text = Strings.Inline.player_card_text.format(user.name if not None else "", user.user_id,
                                                      user.dci if not None else "",
                                                      user.arena if not None else "")
    except DoesNotExist:
        text = Strings.Global.user_not_exist

    results = list()
    results.append(
        InlineQueryResultArticle(
            id="PLAYERCARD",
            title=Strings.Inline.player_card_title,
            description=Strings.Inline.player_card_desc,
            input_message_content=InputTextMessageContent(text, parse_mode=telegram.ParseMode.MARKDOWN)
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


start_pvt_handler = CommandHandler('start', callback=start_pvt, filters=Filters.private)
start_group_handler = CommandHandler('start', callback=start_group, filters=Filters.group)
dci_handler = CommandHandler('dci', callback=dci, filters=Filters.private)
arena_handler = CommandHandler('arena', callback=arena, filters=Filters.private)
name_handler = CommandHandler('name', callback=name, filters=Filters.private)
card_handler = MessageHandler(Filters.regex('\[\[(.*?)\]\]'), cards)
rulings_handler = MessageHandler(Filters.regex('\(\((.*?)\)\)'), rulings)

help_handler = CommandHandler('help', help)
inline_handler = InlineQueryHandler(inline)

dispatcher.add_handler(start_pvt_handler)
dispatcher.add_handler(start_group_handler)
dispatcher.add_handler(dci_handler)
dispatcher.add_handler(arena_handler)
dispatcher.add_handler(name_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(card_handler)
dispatcher.add_handler(rulings_handler)
dispatcher.add_handler(inline_handler)

updater.start_polling(clean=True)
