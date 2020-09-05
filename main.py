# some useful links:
# https://python-telegram-bot.org/
# http://docs.peewee-orm.com/en/latest/peewee/quickstart.html
# https://python-telegram-bot.readthedocs.io/en/stable

from on_pvt import *
from on_group import *
from on_common import *
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, CommandHandler, Filters
import tasks


db = SqliteDatabase(config["database"]["path"])
updater = Updater(token=config["token"], use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


try:
    open(config["database"]["path"])
    logger.info(strings.Log.database_ready)
except FileNotFoundError:
    logger.info(strings.Log.database_not_found)
    db.create_tables([tables.User, tables.Event, tables.Round, tables.Feed])
    logger.log(logging.INFO, strings.Log.database_ok)
finally:
    db.connect()


def error(update, context):
    logger.error('An error occurred! "%s"', context.error)
    raise


def inline(update: Update, context: CallbackContext):
    try:
        user = tables.User.get(tables.User.user_id == update.inline_query.from_user.id)
        text = strings.Inline.player_card_text.format(user.name if not None else "", user.user_id,
                                                      user.dci if not None else "",
                                                      user.arena if not None else "")
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


if config["welcome"]:
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_message))
dispatcher.add_handler(CommandHandler('start', callback=start_pvt, filters=Filters.private))
dispatcher.add_handler(CommandHandler('start', callback=start_group, filters=Filters.group))
dispatcher.add_handler(CommandHandler('rotation', callback=check_rotation, filters=(Filters.private | Filters.group)))
dispatcher.add_handler(CommandHandler('banlist', callback=cards_banlist, filters=(Filters.private | Filters.group)))
dispatcher.add_handler(CommandHandler('social', callback=social_pvt, filters=Filters.private))
dispatcher.add_handler(CommandHandler('social', callback=social, filters=Filters.group))
dispatcher.add_handler(CommandHandler('friendlist', callback=friend_list, filters=Filters.group))
dispatcher.add_handler(CommandHandler('status', callback=arena_status, filters=Filters.group))
dispatcher.add_handler(CommandHandler('dci', callback=dci, filters=Filters.private))
dispatcher.add_handler(CommandHandler('arena', callback=arena, filters=Filters.private))
dispatcher.add_handler(CommandHandler('name', callback=name, filters=Filters.private))
dispatcher.add_handler(CommandHandler('help', callback=help_pvt, filters=Filters.private))
dispatcher.add_handler(MessageHandler(Filters.private and Filters.document, logparser))
dispatcher.add_handler(MessageHandler(Filters.regex('\[\[(.*?)\]\]'), cards))
dispatcher.add_handler(MessageHandler(Filters.regex('\(\((.*?)\)\)'), rulings))
dispatcher.add_handler(MessageHandler(Filters.text & Filters.group, register_users))
dispatcher.add_handler(InlineQueryHandler(inline))
# dispatcher.add_handler(CallbackQueryHandler(callback=help_cb))
dispatcher.add_handler(CallbackQueryHandler(legalities, pattern=r'.*'))

dispatcher.add_error_handler(error)
# start the bot
updater.start_polling(clean=True)

# start the loop to check for rss feeds
loop = asyncio.get_event_loop()
task = loop.create_task(tasks.check_rss(updater))

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
