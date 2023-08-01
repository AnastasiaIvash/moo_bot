
from telebot import TeleBot, types
from .classes import FindListCmd


class FindTopListCmd(FindListCmd):
    """
    Класс для команды, запрашивающей топ песен
    Родитель (FindListCmd)
    """

    _cmd = 'top'

    def __init__(self, bot: TeleBot, message: types.Message) -> None:
        super(FindTopListCmd, self).__init__(bot=bot, message=message)

    def save_song_amt(self, song_amt: int, message: types.Message = None) -> None:
        """
        Метод сохраняет кол-во песен и перенаправляет на метод top_request для создания запроса к api

        :param song_amt: Корректное кол-во песен
        :param message: Последнее сообщение в чате
        """

        super(FindTopListCmd, self).save_song_amt(song_amt=song_amt)
        self.top_request(message=message)


class FindTopCustomListCmd(FindListCmd):
    """
    Класс для команды, запрашивающей топ песен по фильтрам
    Родитель (FindListCmd)
    """

    _cmd = 'top_custom'

    def __init__(self, bot: TeleBot, message: types.Message) -> None:
        super(FindTopCustomListCmd, self).__init__(bot=bot, message=message)

    def save_song_amt(self, song_amt: int, message: types.Message = None) -> None:
        """
        Метод сохраняет кол-во песен и перенаправляет на метод period_keyboard
        для создания клавиатуры для следующих настроек фильтров

        :param song_amt: Корректное кол-во песен
        :param message: Последнее сообщение в чате
        """
        super(FindTopCustomListCmd, self).save_song_amt(song_amt=song_amt)
        self.period_keyboard(message=message)

    def period_keyboard(self, message: types.Message) -> None:
        """
        Метод создает и отправляет клавиатуру для выбора фильтра по временному промежутку

        :param message: Последнее сообщение в чате
        """

        period_markup = types.InlineKeyboardMarkup(row_width=2)
        btn_1 = types.InlineKeyboardButton(text='За день', callback_data='day')
        btn_2 = types.InlineKeyboardButton(text='За неделю', callback_data='week')
        btn_3 = types.InlineKeyboardButton(text='За месяц', callback_data='month')
        btn_4 = types.InlineKeyboardButton(text='За все время', callback_data='all_time')
        period_markup.add(btn_1, btn_2, btn_3, btn_4)

        msg_text = 'За какой промежуток времени вывести топ?'
        self.bot.send_message(chat_id=message.chat.id, text=msg_text, reply_markup=period_markup)

    def genre_keyboard(self, message: types.Message) -> None:
        """
        Метод создает и отправляет клавиатуру для выбора фильтра по жанру

        :param message: Последнее сообщение в чате
        """

        genre_markup = types.InlineKeyboardMarkup(row_width=3)
        btn_1 = types.InlineKeyboardButton(text='Рэп', callback_data='rap')
        btn_2 = types.InlineKeyboardButton(text='Поп', callback_data='pop')
        btn_3 = types.InlineKeyboardButton(text='R&B', callback_data='rb')
        btn_4 = types.InlineKeyboardButton(text='Рок', callback_data='rock')
        btn_5 = types.InlineKeyboardButton(text='Кантри', callback_data='country')
        btn_6 = types.InlineKeyboardButton(text='Любой', callback_data='all')
        genre_markup.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6)

        msg_text = 'Какой жанр выберем?'
        self.bot.send_message(chat_id=message.chat.id, text=msg_text, reply_markup=genre_markup)
