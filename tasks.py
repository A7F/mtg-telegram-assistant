import telegram

from config import config
import feedparser, tables
import asyncio
import logging
import datetime

logger = logging.getLogger(__name__)


async def check_rss(updater):
    urls = config["rss"]["links"]
    limit = config["rss"]["limit"]
    date_3_days_ago = datetime.date.today() - datetime.timedelta(days=config["rss"]["days_until_delete"])
    deleted = tables.Feed.delete().where(tables.Feed.date < date_3_days_ago).execute()
    while True:
        for url in urls:
            feed = feedparser.parse(url)
            if config["rss"]["post_to"]:
                for index, post in zip(range(limit), feed.entries):
                    try:
                        rss = tables.Feed.get(tables.Feed.feed_id == post.id)
                    except tables.DoesNotExist:
                        try:
                            x = datetime.datetime(*post.updated_parsed[:6])
                        except AttributeError:
                            x = datetime.datetime.today()
                        finally:
                            tables.Feed.create(feed_id=post.id, date=x)
                            text = "[" + post.title + "](" + post.link + ")"
                            if config["rss"]["post_to"] == "channel":
                                updater.bot.send_message(chat_id=config["channel_id"],
                                                         text=text,
                                                         parse_mode=telegram.ParseMode.MARKDOWN)
                            else:
                                updater.bot.send_message(chat_id=config["group_id"],
                                                         text=text,
                                                         parse_mode=telegram.ParseMode.MARKDOWN)
        await asyncio.sleep(config["rss"]["poll_time"])