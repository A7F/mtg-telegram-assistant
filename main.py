# some useful links:
# https://python-telegram-bot.org/
# http://docs.peewee-orm.com/en/latest/peewee/quickstart.html
# https://python-telegram-bot.readthedocs.io/en/stable

import logging, json, telegram, tables, scrython, re, asyncio, time, strings, util
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ChatAction
from peewee import *
from emoji import emojize
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, CommandHandler, Filters


with open('config/config.json', "r+") as f:
    f.seek(0)
    config = json.load(f)

db = SqliteDatabase(config["database"]["path"])
updater = Updater(token=config["token"])
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
max_cards = 4

try:
    open(config["database"]["path"])
    logging.info(strings.Log.database_ready)
except FileNotFoundError:
    logging.info(strings.Log.database_not_found)
    db.create_tables([tables.User, tables.Event, tables.Round])
    logging.log(logging.INFO, strings.Log.database_ok)
finally:
    db.connect()


def start_pvt(bot, update):
    try:
        user = tables.User.get(tables.User.user_id == update.message.from_user.id)
        text = strings.Start.start_pvt
    except DoesNotExist:
        text = strings.Global.user_not_exist
    finally:
        text += strings.Start.start_id.format(update.message.from_user.id)
        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)


def start_group(bot, update):
    util.get_admin_ids(bot, update.message.chat_id)
    try:
        user = tables.User.get(tables.User.user_id == update.message.from_user.id)
        bot.send_message(chat_id=update.message.chat_id, text=strings.Global.user_already_exist)
    except DoesNotExist:
        member = tables.User.create(user_id=update.message.from_user.id, group=update.message.chat_id,
                                    name=update.message.from_user.first_name)
        bot.send_message(chat_id=update.message.chat_id, text=strings.Global.welcome, parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def dci(bot, update):
    args = update.message.text.split(" ")
    if len(args) == 1:
        text = strings.Dci.dci_invalid
    else:
        dci = args[1]
        try:
            if dci.isdigit() and not dci.startswith('-'):
                user = tables.User.get(tables.User.user_id == update.message.from_user.id)
                user.dci = dci
                user.save()
                text = strings.Dci.dci_set.format(dci)
            else:
                text = strings.Dci.dci_invalid
        except DoesNotExist:
            text = strings.Global.user_not_exist
    bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def name(bot, update):
    args = update.message.text.split(" ")
    if len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text=strings.Name.name_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        name = args[1]
        try:
            user = tables.User.get(tables.User.user_id == update.message.from_user.id)
            user.name = name
            user.save()
            bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Name.name_set.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def arena(bot, update):
    args = update.message.text.split(" ")
    if len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text=strings.Arena.arena_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        arena = args[1]
        try:
            user = tables.User.get(tables.User.user_id == update.message.from_user.id)
            user.arena = arena
            user.save()
            bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Arena.arena_set.format(arena),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.UPLOAD_PHOTO)
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
                             text=strings.Card.card_not_found.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
            continue
        not_legal = [k for k, v in card.legalities().items() if v == "not_legal"]
        legal_in = ""
        if len(not_legal) == 0:
            legal_in = strings.Card.card_legal
        else:
            for v in not_legal:
                legal_in += v + " "
        try:
            eur = card.currency(mode="eur") + "€"
        except KeyError:
            eur = strings.Card.card_unavailable
        try:
            usd = card.currency(mode="usd") + "$"
        except KeyError:
            usd = strings.Card.card_unavailable

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


@util.send_action(ChatAction.TYPING)
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
                             text=strings.Card.card_not_found.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
            continue
        rule = scrython.rulings.Id(id=card.id())
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        message = ""
        if rule.data_length() == 0:
            message = strings.Card.card_ruling_unavailable
        else:
            for index, rule_text in enumerate(rule.data()):
                message += (str(index + 1) + ". " + rule.data(index=index, key="comment") + "\n\n")
        bot.send_message(chat_id=update.message.chat_id, text=message, reply_to_message_id=update.message.message_id)
        time.sleep(0.07)


@util.send_action(ChatAction.TYPING)
def help_pvt(bot, update):
    if update.message.from_user.id in util.get_admin_ids(bot):
        button_list = [InlineKeyboardButton("user", callback_data="help_user"),
                       InlineKeyboardButton("admin", callback_data="help_admin")]
        reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
        text = strings.Help.admin_help
        bot.send_message(chat_id=update.message.chat_id,
                         text=emojize(text, use_aliases=True),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)
    else:
        text = strings.Help.user_help
        bot.send_message(chat_id=update.message.chat_id,
                         text=emojize(text, use_aliases=True),
                         parse_mode=telegram.ParseMode.MARKDOWN)


def help_cb(bot, update):
    query = update.callback_query
    button_list = [InlineKeyboardButton("user", callback_data="help_user"),
                   InlineKeyboardButton("admin", callback_data="help_admin")]
    reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
    if "help_user" in query.data:
        reply = strings.Help.user_help
        pass
    else:
        reply = strings.Help.admin_help
        pass
    try:
        bot.edit_message_text(text=reply, chat_id=query.message.chat_id,
                              message_id=query.message.message_id, reply_markup=reply_markup,
                              parse_mode=telegram.ParseMode.MARKDOWN)
    except telegram.error.BadRequest:
        bot.answer_callback_query(callback_query_id=update.callback_query.id)


def inline(bot, update):
    query = update.inline_query.query
    try:
        user = tables.User.get(tables.User.user_id == update.inline_query.from_user.id)
        pw_url = "https://www.wizards.com/Magic/PlaneswalkerPoints/"
        text = strings.Inline.player_card_text.format(user.name if not None else "", user.user_id,
                                                      user.dci if not None else "",
                                                      user.arena if not None else "",
                                                      pw_url + str(user.dci) if not None else pw_url)
    except DoesNotExist:
        text = strings.Global.user_not_exist

    results = list()
    results.append(
        InlineQueryResultArticle(
            id="PLAYERCARD",
            title=strings.Inline.player_card_title,
            description=strings.Inline.player_card_desc,
            input_message_content=InputTextMessageContent(text,
                                                          parse_mode=telegram.ParseMode.MARKDOWN,
                                                          disable_web_page_preview=True)
        )
    )
    bot.answer_inline_query(update.inline_query.id, results, cache_time=10)


dispatcher.add_handler(CommandHandler('start', callback=start_pvt, filters=Filters.private))
dispatcher.add_handler(CommandHandler('start', callback=start_group, filters=Filters.group))
dispatcher.add_handler(CommandHandler('dci', callback=dci, filters=Filters.private))
dispatcher.add_handler(CommandHandler('arena', callback=arena, filters=Filters.private))
dispatcher.add_handler(CommandHandler('name', callback=name, filters=Filters.private))
dispatcher.add_handler(CommandHandler('help', callback=help_pvt, filters=Filters.private))
dispatcher.add_handler(MessageHandler(Filters.regex('\[\[(.*?)\]\]'), cards))
dispatcher.add_handler(MessageHandler(Filters.regex('\(\((.*?)\)\)'), rulings))
dispatcher.add_handler(InlineQueryHandler(inline))
dispatcher.add_handler(CallbackQueryHandler(callback=help_cb))

updater.start_polling(clean=True)
