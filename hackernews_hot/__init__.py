import asyncio
import configparser
import time

from .database import StoryHandler
from .hackernews import HackerNewsFetcher
from .telegram import TelegramBot

config = configparser.ConfigParser()
config.read("config.ini")


def create_hackernews_fetcher():
    bot_token = config["telegram"]["token"]
    bot_chat_id = config["telegram"]["chat_id"]
    database_uri = config["database"]["uri"]
    score_threshold = int(config["common"]["score_threshold"])

    telegram_bot = TelegramBot(token=bot_token, chat_id=bot_chat_id)
    story_handler = StoryHandler(database_uri, telegram_bot)
    hackernews_fetcher = HackerNewsFetcher(
        score_target=score_threshold, story_handler=story_handler
    )
    return hackernews_fetcher


def cron():
    interval_mins = int(config["common"]["interval_mins"])
    hackernews_fetcher = create_hackernews_fetcher()
    while True:
        asyncio.run(hackernews_fetcher.run_task())
        time.sleep(60 * interval_mins)
