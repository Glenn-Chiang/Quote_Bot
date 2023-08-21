import asyncio
from dotenv import load_dotenv
load_dotenv()
import os
import requests
from telegram.constants import ParseMode
from telegram import Bot 
import sys

async def main():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    base_url = os.getenv('BASE_URL')
    
    response = None
    try:
        response = requests.get(f'{base_url}/quotes/random')
        response.raise_for_status()

    except requests.exceptions.HTTPError as error:
        print(error['error'])
        sys.exit()

    quote = response.json()['content']
    author_name = response.json()['author']['name']

    formatted_quote = f"{quote}\n\n- <i>{author_name}</i>"
    await bot.send_message(chat_id=os.getenv('CHANNEL_ID'), text=formatted_quote, parse_mode=ParseMode.HTML)
    print(formatted_quote)


def lambda_handler(event, context):
    asyncio.run(main())


if __name__ == '__main__':
    asyncio.run(main())