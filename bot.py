import os
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
import exceptions
import logging
from logging.handlers import RotatingFileHandler

from generate import TextGenerator

# Загрузка переменных из .env файла
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Инициализация бота
updater = Updater(token=TELEGRAM_TOKEN)

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
)
handler = RotatingFileHandler(
    'main.log',
    maxBytes=50000000,
    backupCount=5,
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s -'
                                       ' %(levelname)s -'
                                       ' %(message)s'))
logger.addHandler(handler)


def generate_text(update, context):
    """Генерирует текст и отправляет его пользователю в чат."""
    chat = update.effective_chat
    try:
        text = TextGenerator().generate()
        context.bot.send_message(chat_id=chat.id, text=text)
        logger.info(f'Отправлено сообщение {text}'
                    f' пользователю: {TELEGRAM_CHAT_ID}')
    except exceptions.SendMessageException as e:
        logger.error(f'Ошибка при отправке сообщения: {e}')


def wake_up(update, context):
    """Приветствует пользователя и предоставляет кнопку для генерации
    текста. """
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Генерировать предложение']])
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет {name}, я умею генерировать текст!!',
        reply_markup=button
    )


def text_message(update, context):
    """Отправляет сообщение пользователю о необходимости использовать
    кнопку."""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text="Используйте кнопку для взаимодействия.")


if __name__ == "__main__":
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex(r'Генерировать предложение'), generate_text))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()
