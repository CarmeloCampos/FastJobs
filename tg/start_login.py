from telegram import Update
from telegram.ext import ContextTypes

from lib.tiny import short_url
from sis.bot import flex
from sis.config import set_flex_data, get_flex_data
from sis.lang import langFile
from tg.menu import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    if flex.needLogin():
        await update.message.reply_text(langFile['needLogin'])
        link, verifier = flex.generate_challenge_link()
        short_link = short_url(link)
        body = langFile['loginSteep']['step0'] + ' ' + short_link
        body += "\n\n" + langFile['loginSteep']['step1']
        body += "\n" + langFile['loginSteep']['step2']
        body += "\n" + langFile['loginSteep']['step3']
        body += "\n\n<i>" + langFile['loginSteep']['example'] + "</i>"
        await update.message.reply_video(video="https://carmelocampos.com/cdn/FastJobsIntro-1.mp4", caption=body,
                                         parse_mode='HTML')
        await update.message.reply_text(langFile['toCancel'])
        set_flex_data('waiting_login', True)
        set_flex_data('code_verifier', verifier)
        return 'LOGIN'
    else:
        await update.message.reply_text(langFile['readyLogin'], reply_markup=main_menu)
        set_flex_data('ready_login', True)


async def login(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    waiting_login = get_flex_data('waiting_login')
    code_verifier = get_flex_data('code_verifier')
    if waiting_login:
        try:
            if flex.registerAccount(update.message.text, code_verifier):
                await update.message.reply_text(langFile['loggedin'], reply_markup=main_menu)
                set_flex_data('ready_login', True)
            else:
                await update.message.reply_text(langFile['errorLogin'])
        except Exception as e:
            print('Error in login', e)
            await update.message.reply_text(langFile['errorLogin'])
    else:
        await update.message.reply_text(langFile['noNeedLogin'], reply_markup=main_menu)
