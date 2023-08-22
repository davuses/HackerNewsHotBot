import json
import logging
import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)


class TooManyRequests(Exception):
    ...


class TelegramBot:
    BASE_URL = "https://api.telegram.org/bot{token}/{method}"

    def __init__(self, token, chat_id) -> None:
        self.token = token
        self.chat_id = chat_id

    @retry(
        retry=retry_if_exception_type(TooManyRequests),
        stop=stop_after_attempt(3),
        wait=wait_fixed(31),
    )
    def send_message(
        self,
        text,
        reply_markup=None,
        parse_mode="HTML",
        disable_notification=True,
    ):
        message = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification,
        }

        if reply_markup:
            message["reply_markup"] = reply_markup

        try:
            result = httpx.post(
                self.BASE_URL.format(token=self.token, method="sendMessage"),
                json=message,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
        except httpx.TimeoutException as e:
            logging.exception(e)
            return None
        if result.status_code == 200:
            return json.loads(result.content)
        if result.status_code == 429:
            raise TooManyRequests
        else:
            logging.error(result.content)
            return None
