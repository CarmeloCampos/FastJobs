from telegram.ext import Application

from sis.config import configFile
from sis.lang import langFile


async def set_commands(app: Application) -> None:
    await app.bot.set_my_commands([
        ('start', langFile['start']),
    ])


application = Application.builder().token(configFile["telegramToken"]).post_init(set_commands).build()
