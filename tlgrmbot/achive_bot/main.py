from logging import getLogger

from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.utils.request import Request

from echo.config import load_config


def main():
    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token='1078809721:AAGHvwEiWVgHO8M9Q2N2SC_DyPqXo-pUaQ0',
        request=req,
        base_url='https://telegg.ru/orig/bot',
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )
    info = bot.get_me()


if __name__ == '__main__':
    main()
