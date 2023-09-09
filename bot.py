import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup

from generate import generate

load_dotenv()

updater = Updater(token=os.getenv('TELEGRAM_TOKEN'))


def generate_text(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=generate())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Генерировать предложение']])
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет {name}, я умею генерировать текст!!',
        reply_markup=button
    )


updater.dispatcher.add_handler(CommandHandler('start', wake_up))

updater.dispatcher.add_handler(MessageHandler(Filters.text, generate_text))

updater.start_polling()
updater.idle()
