import os
import asyncio
import logging

from globals import run_app

bot_token = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    asyncio.run(run_app(bot_token))
