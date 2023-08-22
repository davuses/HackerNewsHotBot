# coding: utf-8

import datetime
import logging

import timeago
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from .telegram import TelegramBot

FOUR_HOURS = datetime.timedelta(hours=4)
TWO_DAYS = datetime.timedelta(days=2)


Base = declarative_base()


class StoryPost(Base):
    __tablename__ = "story_post"

    id = Column(String, primary_key=True)  # Assuming 'id' is a string
    title = Column(String)
    text = Column(Text)
    message = Column(Text)
    url = Column(Text)
    story_url = Column(Text)
    hn_url = Column(Text)
    score = Column(Integer)
    telegram_message_id = Column(Integer)
    created = Column(DateTime, default=datetime.datetime.utcnow)


class StoryHandler:
    def __init__(self, database_uri: str, telegram_bot: TelegramBot) -> None:
        self.engine = create_engine(database_uri)
        Base.metadata.create_all(self.engine)
        self.telegram_bot = telegram_bot

    def add_story(self, story):
        with Session(self.engine) as session:
            story_id_int = story.get("id")
            story_id = str(story_id_int)
            hn_url = "https://news.ycombinator.com/item?id={}".format(story_id)
            story_url = story.get("url")

            post = session.query(StoryPost).get(story_id)
            if post:
                logging.info(f"STOP: {story_id} in DB")
                return
            logging.info("SEND: {}".format(story_id))

            story["title"] = story.get("title")
            comments_count = story.get("descendants", 0)
            buttons = []

            if story_url:
                buttons.append({"text": "Read", "url": story_url})
            story["url"] = hn_url

            buttons.append(
                {"text": "{}+ Comments".format(comments_count), "url": hn_url}
            )

            now = datetime.datetime.now()
            published = datetime.datetime.fromtimestamp(story.get("time"))
            ago = timeago.format(now, published)

            # Add 🔥 emoji if story is hot and gained required score in less than 2 hours,
            # or add ❄️ if it took it more than 2 days
            status_emoji = ""
            delta = now - published
            if delta <= FOUR_HOURS:
                status_emoji = "🔥 "
            elif delta >= TWO_DAYS:
                status_emoji = "❄️ "

            # Add title
            message = (
                "<b>{title}</b> ({status_emoji}Score: {score}+ {ago})\n\n"
                .format(ago=ago, status_emoji=status_emoji, **story)
            )

            # Add link
            message += "<b>Link:</b> {}\n".format(story_url)

            # Add comments Link(don't add it for `Ask HN`, etc)
            if story_url:
                message += "<b>Comments:</b> {}\n".format(hn_url)

            # Add text
            text = story.get("text")
            if text:
                text = (
                    text.replace("<p>", "\n")
                    .replace("&#x27;", "'")
                    .replace("&#x2F;", "/")
                )
                message += "\n{}\n".format(text)

            # Send to the telegram channel
            result = self.telegram_bot.send_message(
                message, {"inline_keyboard": [buttons]}
            )

            logging.info("Telegram response: {}".format(result))

            telegram_message_id = None
            if result and result.get("ok"):
                telegram_message_id = result.get("result").get("message_id")
            print("{id} pushed to channel ({score})".format(**story))
            new_story = StoryPost(
                id=story_id,
                title=story.get("title"),
                url=story_url,
                score=story.get("score"),
                text=story.get("text"),
                story_url=story_url,
                hn_url=hn_url,
                message=message,
                telegram_message_id=telegram_message_id,
            )
            session.add(new_story)
            session.commit()
