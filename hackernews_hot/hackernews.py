import logging

import httpx
from tqdm.asyncio import tqdm


class HackerNewsFetcher:
    BASE_URL = "https://hacker-news.firebaseio.com/v0/{method}.json"

    def __init__(self, score_target, story_handler) -> None:
        self.score_target = score_target
        self.cached_stories_id = set()
        self.story_handler = story_handler

    async def fetch_url(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            if response.status_code == 200:
                return response.content
            return None

    async def top_stories(
        self,
    ):
        async with httpx.AsyncClient() as client:
            url = self.BASE_URL.format(method="topstories")
            response = await client.get(url, timeout=10)
            data = response.json()
            return data

    async def get_story(self, item_id, client):
        url = self.BASE_URL.format(method=f"item/{item_id}")
        response = await client.get(url, timeout=10)
        data = response.json()
        return data

    async def get_stories(self, item_ids):
        async with httpx.AsyncClient() as client:
            tasks = [self.get_story(item_id, client) for item_id in item_ids]

            items = await tqdm.gather(*tasks)
            return items

    def check_story(self, story):
        try:
            story_id = story.get("id")
            if story and story.get("score") >= self.score_target:
                logging.info(
                    "{id} reaches score threshold ({score})".format(**story)
                )
                self.story_handler.add_story(story)
                self.cached_stories_id.add(story_id)
            elif story and story.get("score"):
                logging.info(
                    "STOP: {id} has low score ({score})".format(**story)
                )
            elif story:
                logging.info("STOP: {id} has no score".format(**story))
            else:
                logging.info("STOP: story was probably deleted/flagged")
        except Exception as ex:
            logging.exception(ex)

    async def check_stories(self, top_story_ids):
        ids = set(str(story_id) for story_id in top_story_ids)
        logging.info("checking stories: {}".format(ids))
        logging.info("cached stories: {}".format(self.cached_stories_id))
        stories_id_to_check = ids.difference(self.cached_stories_id)
        stories = await self.get_stories(stories_id_to_check)
        for story in stories:
            self.check_story(story)

    async def run_task(self):
        top_story_ids = await self.top_stories()
        await self.check_stories(top_story_ids)
