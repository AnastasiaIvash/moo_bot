
import re

from telebot import TeleBot, types

HELLO = ['привет', 'прив', 'хай']


def text_response(bot: TeleBot, message: types.Message) -> None:
    """
    Фильтрует текстовое сообщение пользователя на наличие слов из словаря

    :param bot: Бот
    :param message: Последнее сообщение в чате
    """

    for patt in HELLO:
        if re.findall(patt, message.text.lower()):
            start(bot=bot, message=message)
    else:
        bot.send_message(chat_id=message.chat.id, text='Попробуй /help')


def start(bot: TeleBot, message: types.Message) -> None:
    """
    Отправляет приветственное сообщение

    :param bot: Бот
    :param message: Последнее сообщение в чате
    """

    msg_text = 'Привет! Меня зовут Муу, и я бот, который знает обо всех мировых хитах и об их исполнителях :)\n' \
               'Я всего лишь учебный проект, но, думаю, у меня большой потенциал! Попробуй комманду /help, чтобы ' \
               'посмотреть, что я умею.'
    bot.send_message(chat_id=message.chat.id, text=msg_text, parse_mode='HTML')


def help(bot: TeleBot, message: types.Message) -> None:
    """
    Отправляет сообщение со списком комманд

    :param bot: Бот
    :param message: Последнее сообщение в чате
    """

    msg_text = 'Итак, давай посмотрим, что я могу:\n' \
               '/top - делюсь с тобой лучшими песнями за все время.\n' \
               '/top_custom - и получишь список лучших песен, которые соответствуют твоим предпочтениям.\n' \
               '/random - сыграем в рулетку? я поделюсь с тобой случайной песней!\n' \
               '/about - на случай, если ты захочешь узнать больше о каком-то конкретном треке.\n' \
               '/lyrics - могу показать даже текст песни!\n' \
               '/artist - показываю информацию об интересном тебе артисте.\n' \
               '/history - история поиска.'
    bot.send_message(chat_id=message.chat.id, text=msg_text)
