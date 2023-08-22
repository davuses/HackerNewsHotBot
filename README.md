# HackerNews Hot Bot

HackerNews Hot Bot is a Telegram bot that automatically shares the latest hot stories from Hacker News with your Telegram channel or chat.

This project was inspired by [hackernewsbot](https://github.com/phil-r/hackernewsbot).

## Features

- Fetches the latest top stories from [Hacker News](https://news.ycombinator.com) every 30 minutes.
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
token=<bot_token>
# channel or chat id
chat_id=<chat_id>

[database]
uri=sqlite:///stories.db

[common]
# score threshold
score_threshold=300
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
