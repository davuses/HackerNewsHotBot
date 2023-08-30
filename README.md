# HackerNews Hot Bot

HackerNews Hot Bot is a Telegram bot that automatically shares the latest hot stories from Hacker News with your Telegram channel or chat.

This project was inspired by [hackernewsbot](https://github.com/phil-r/hackernewsbot).

## Features

- Fetches the latest top stories from [Hacker News](https://news.ycombinator.com) every 30 minutes. You can customize the update interval to suit your needs.
- Posts stories that meet a certain score threshold, adjusted for inflation, ensuring high-quality content.

## Prerequisites

Before getting started, you'll need the following:

- A Telegram bot token: Create a bot on Telegram and obtain the API token.
- Chat ID: Identify the channel or chat where you want to post the Hacker News stories.
- Python: Make sure you have Python installed on your system.

## Installation

1. Clone this repository to your local machine

2. Create a configuration file named `config.ini` and provide your Telegram bot token, chat ID, and other settings as follows:

```ini
[telegram]
; Telegram Bot Token:
;   Insert your Telegram Bot API token here.
token=<bot_token>

; Channel or Chat ID:
;   Specify the target channel or chat where the bot will post stories.
chat_id=<chat_id>

[database]
; Specify the URI for the database.
uri=sqlite:///stories.db

[common]
; Score Threshold:
;   Defines the minimum score a Hacker News story must have to be posted.
score_threshold=280

; Update Interval (in minutes):
;   Specifies how often the bot fetches the latest stories from Hacker News.
interval_mins=60
```

3. Install the required Python packages:

```sh
pip install -r requirements.txt
```

### Usage

To run the HackerNews Hot Bot, execute the following command within the project directory:

```sh
python run.py
```
