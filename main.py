# some useful links:
# https://python-telegram-bot.org/
# http://docs.peewee-orm.com/en/latest/peewee/quickstart.html
# https://python-telegram-bot.readthedocs.io/en/stable

import logging, telegram, tables, scrython, re, asyncio, time, strings, util
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import ChatAction
from peewee import *
from emoji import emojize
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import MessageHandler, CommandHandler, Filters
import feedparser, datetime, logging
from config import config

db = SqliteDatabase(config["database"]["path"])
updater = Updater(token=config["token"], use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
max_cards = 4

try:
    open(config["database"]["path"])
    logging.info(strings.Log.database_ready)
except FileNotFoundError:
    logging.info(strings.Log.database_not_found)
    db.create_tables([tables.User, tables.Event, tables.Round, tables.Feed])
    logging.log(logging.INFO, strings.Log.database_ok)
finally:
    db.connect()


async def check_rss():
    urls = config["rss"]["links"]
    limit = config["rss"]["limit"]
    while True:
        for url in urls:
            feed = feedparser.parse(url)
            for index, post in zip(range(limit), feed.entries):
                try:
                    rss = tables.Feed.get(tables.Feed.feed_id == post.id)
                except DoesNotExist:
                    try:
                        x = datetime.datetime(*post.updated_parsed[:6])
                    except AttributeError:
                        x = datetime.datetime.today()
                    finally:
                        tables.Feed.create(feed_id=post.id, date=x)
                        text = "[" + post.title + "](" + post.link + ")"
                        if config["group_id"] == 0:
                            pass
                        else:
                            updater.bot.send_message(chat_id=config["group_id"], text=text,
                                                     parse_mode=telegram.ParseMode.MARKDOWN)
        await asyncio.sleep(config["rss"]["poll_time"])


def error(update, context):
    logger.warning('Error "%s"', context.error)


def start_pvt(update: Update, context: CallbackContext):
    try:
        tables.User.get(tables.User.user_id == update.message.from_user.id)
        text = strings.Start.start_pvt
    except DoesNotExist:
        text = strings.Global.user_not_exist
    finally:
        text += strings.Start.start_id.format(update.message.from_user.id)
        context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)


def start_group(update: Update, context: CallbackContext):
    try:
        tables.User.get(tables.User.user_id == update.message.from_user.id)
        context.bot.send_message(chat_id=update.message.chat_id, text=strings.Global.user_already_exist)
    except DoesNotExist:
        tables.User.create(user_id=update.message.from_user.id,
                           group=update.message.chat_id,
                           name=update.message.from_user.first_name)
        welcome = strings.Global.welcome.format(update.message.chat_id)
        context.bot.send_message(chat_id=update.message.chat_id, text=welcome, parse_mode=telegram.ParseMode.MARKDOWN)


def friend_list(update: Update, context: CallbackContext):
    query = tables.User.select().where(tables.User.arena.is_null(False))
    text = strings.Friendlist.friendlist+"\n"
    for result in query:
        chat_member = context.bot.getChatMember(chat_id=update.message.chat_id, user_id=result.user_id)
        user = chat_member.user
        if user is None:
            result.delete()
            continue
        else:
            if user.username:
                text += "[{}](t.me/{}) - {}\n".format(result.name, user.username, result.arena)
            else:
                text += "{} - {}\n".format(result.name, result.arena)
    context.bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     parse_mode=telegram.ParseMode.MARKDOWN,
                     disable_web_page_preview=True)


@util.send_action(ChatAction.TYPING)
def dci(update: Update, context: CallbackContext):
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
    context.bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def name(update: Update, context: CallbackContext):
    args = update.message.text.split(" ", 1)
    if len(args) == 1:
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=strings.Name.name_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        name = args[1]
        try:
            user = tables.User.get(tables.User.user_id == update.message.from_user.id)
            user.name = name
            user.save()
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Name.name_set.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def arena(update: Update, context: CallbackContext):
    args = update.message.text.split(" ", 1)
    if len(args) == 1:
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=strings.Arena.arena_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        arena = args[1]
        try:
            user = tables.User.get(tables.User.user_id == update.message.from_user.id)
            user.arena = arena
            user.save()
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Arena.arena_set.format(arena),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.UPLOAD_PHOTO)
def cards(update: Update, context: CallbackContext):
    match = re.findall(r'\[\[(.*?)\]\]', update.message.text)
    asyncio.set_event_loop(asyncio.new_event_loop())
    for index, name in enumerate(match):
        if index > max_cards:
            break
        try:
            card = scrython.cards.Named(fuzzy=name)
        except Exception:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Card.card_not_found.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
            continue
        banned_in = [k for k, v in card.legalities().items() if v == "banned"]
        legal_in = ""
        if len(banned_in) == 0:
            legal_in = strings.Card.card_legal
        else:
            for v in banned_in:
                legal_in += v + " "
        try:
            eur = card.prices(mode="eur") + "€"
        except (KeyError, TypeError):
            eur = "CardMarket"
        try:
            usd = card.prices(mode="usd") + "$"
        except (KeyError, TypeError):
            usd = "TCGPlayer"

        usd_link = card.purchase_uris().get("tcgplayer")
        eur_link = card.purchase_uris().get("cardmarket")
        if eur_link is None or card.lang() == config["locale"]:
            eur_link = "https://www.cardmarket.com/" + config["locale"] \
                       + "/Magic/Products/Search?searchString=" + name.replace(" ", "+")
        if usd_link is None:
            usd_link = "https://shop.tcgplayer.com/productcatalog/product/show?newSearch=false&ProductName=" \
                       + name.replace(" ", "+")

        edhlink = "https://edhrec.com/cards/" + name.replace(" ", "-") if card.lang() == "en" else "https://edhrec.com"
        img_caption = emojize(":moneybag: [" + eur + "]" + "(" + eur_link + ")" + " | "
                              + "[" + usd + "]" + "(" + usd_link + ")" + "\n"
                              + ":no_entry: " + legal_in + "\n"
                              + "[EDHREC](" + edhlink + ")", use_aliases=True)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=card.image_uris(0, image_type="normal"),
                       caption=img_caption, parse_mode=telegram.ParseMode.MARKDOWN,
                       reply_to_message_id=update.message.message_id)
        time.sleep(0.04)


@util.send_action(ChatAction.TYPING)
def rulings(update: Update, context: CallbackContext):
    match = re.findall(r'\(\((.*?)\)\)', update.message.text)
    asyncio.set_event_loop(asyncio.new_event_loop())
    for index, name in enumerate(match):
        if index > max_cards:
            break
        try:
            card = scrython.cards.Named(fuzzy=name)
        except Exception:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Card.card_not_found.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
            continue
        rule = scrython.rulings.Id(id=card.id())
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        message = ""
        if rule.data_length() == 0:
            message = strings.Card.card_ruling_unavailable
        else:
            for index, rule_text in enumerate(rule.data()):
                message += (str(index + 1) + ". " + rule.data(index=index, key="comment") + "\n\n")
        context.bot.send_message(chat_id=update.message.chat_id, text=message, reply_to_message_id=update.message.message_id)
        time.sleep(0.07)


def register_users(update: Update, context: CallbackContext):
    try:
        tables.User.get(tables.User.user_id == update.message.from_user.id)
    except DoesNotExist:
        tables.User.create(user_id=update.message.from_user.id,
                           group=update.message.chat_id,
                           name=update.message.from_user.first_name)


@util.send_action(ChatAction.TYPING)
def help_pvt(update: Update, context: CallbackContext):
    if update.message.from_user.id in util.get_admin_ids(context.bot):
        button_list = [InlineKeyboardButton("user", callback_data="help_user"),
                       InlineKeyboardButton("admin", callback_data="help_admin")]
        reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
        text = strings.Help.admin_help
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=emojize(text, use_aliases=True),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)
    else:
        text = strings.Help.user_help
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=emojize(text, use_aliases=True),
                         parse_mode=telegram.ParseMode.MARKDOWN)


def help_cb(update: Update, context: CallbackContext):
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
        context.bot.edit_message_text(text=reply, chat_id=query.message.chat_id,
                              message_id=query.message.message_id, reply_markup=reply_markup,
                              parse_mode=telegram.ParseMode.MARKDOWN)
    except telegram.error.BadRequest:
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)


def inline(update: Update, context: CallbackContext):
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
    context.bot.answer_inline_query(update.inline_query.id, results, cache_time=10)


dispatcher.add_handler(CommandHandler('start', callback=start_pvt, filters=Filters.private))
dispatcher.add_handler(CommandHandler('start', callback=start_group, filters=Filters.group))
dispatcher.add_handler(CommandHandler('friendlist', callback=friend_list, filters=Filters.group))
dispatcher.add_handler(CommandHandler('dci', callback=dci, filters=Filters.private))
dispatcher.add_handler(CommandHandler('arena', callback=arena, filters=Filters.private))
dispatcher.add_handler(CommandHandler('name', callback=name, filters=Filters.private))
dispatcher.add_handler(CommandHandler('help', callback=help_pvt, filters=Filters.private))
dispatcher.add_handler(MessageHandler(Filters.regex('\[\[(.*?)\]\]'), cards))
dispatcher.add_handler(MessageHandler(Filters.regex('\(\((.*?)\)\)'), rulings))
dispatcher.add_handler(MessageHandler(Filters.text & Filters.group, register_users))
dispatcher.add_handler(InlineQueryHandler(inline))
dispatcher.add_handler(CallbackQueryHandler(callback=help_cb))

dispatcher.add_error_handler(error)
# start the bot
updater.start_polling(clean=True)

# start the loop to check for rss feeds
loop = asyncio.get_event_loop()
task = loop.create_task(check_rss())

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
