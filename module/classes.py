import requests

from datetime import datetime
from telebot import TeleBot, types
from .history.model_class import DB as db, User, Command

from typing import List, Dict


class Cmd:
    """
    Родительский класс, представляющий собой объект,
    хранящий информацию о команде и исполняющий ее

    Attributes:
        _cmd (str): Название команды
        _headers (Dict[str]): Словарь, хранящий в себе информацию о хидерах для запросов к api
        _result (None, str): Хранит информацию о полученном результате после выполнения команды

        _time_request (str): Дата и время запуска команды
        _user_id (int): ID пользователя, с которым ведется переписка
        bot (TeleBot): Бот

    """

    _cmd = ''
    _headers = {
        "X-RapidAPI-Key": "4b86c8ee23msh7069dd41f0b5bd0p1f0ef6jsnbc57b3fde1e8",
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    _result = None

    def __init__(self, bot: TeleBot, message: types.Message, user_id: int = None) -> None:
        self._time_request = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if user_id is None:
            self._user_id = message.from_user.id
        else:
            self._user_id = user_id

        self.bot = bot

    def _save_history(self) -> None:
        """
        Завершающий метод для сохранения информации о произведенной команде в БД
        """

        with db:
            db.create_tables([User, Command])

            get_user = User.get_or_create(user_id=self._user_id)[0]
            new_command = Command.create(cmd_name=self._cmd, created_at=self._time_request,
                                         result=self._result, user=get_user)
            new_command.save()


class FindCmd(Cmd):
    """
    Родительский класс для команд, запрашивающих информацию об одном объекте из api
    (Родитель Cmd)

    Attributes:
        pattern (None, str): Шаблон, полученный от пользователя, по которому производится поиск
        id (None, int): ID искомого объекта
    """

    pattern = None
    id = None

    def __init__(self, bot: TeleBot, message: types.Message, user_id: int = None) -> None:
        super(FindCmd, self).__init__(bot=bot, message=message, user_id=user_id)

    def _find_list_request(self, page: int = 1) -> Dict:
        """
        Метод делает запрос к api по полученному шаблону и возвращает словарь со списком значений

        :param page: Номер страницы для поиска
        :return response: Словарь с полученным ответом от api
        """

        url = "https://genius-song-lyrics1.p.rapidapi.com/search/multi/"
        querystring = {"q": self.pattern, "per_page": "5", "page": str(page)}
        response = requests.get(url, headers=self._headers, params=querystring).json()
        return response

    def start_cmd_for_no_id(self, message: types.Message, start_msg: str) -> None:
        """
        Метод отправляет первое сообщение и перенаправляет полученное сообщение к методу find_list

        :param message: Последнее сообщение в чате
        :param start_msg: Первое сообщение пользователю
        """
        msg_text = start_msg
        next_msg = self.bot.send_message(chat_id=message.chat.id, text=msg_text)
        self.bot.register_next_step_handler(message=next_msg, callback=self.find_list)

    def find_list(self, message: types.Message, page: int = 1) -> Dict:
        """
        Функция отправляет шаблон поиска и получает ответ от _find_list_request

        :param message: Последнее сообщение в чате
        :param page: Номер страницы
        :return response: Словарь с полученным ответом от api
        """
        if not self.pattern:
            self.pattern = message.text.lower()
        response = self._find_list_request(page=page)
        return response


class FindListCmd(Cmd):
    """
    Родительский класс для команд, запрашивающих список песен
    (Родитель Cmd)

    Attributes:
        song_amt (int): Кол-во песен для вывода
        time_period (str): Фильтр для поиска по времени
        genre (str): Фильтр для поиска по жанрам
    """

    song_amt = 0
    time_period = 'all_time'
    genre = 'all'

    def __init__(self, bot: TeleBot, message: types.Message) -> None:
        super(FindListCmd, self).__init__(bot=bot, message=message)
        self.start_message(message=message)

    def start_message(self, message) -> None:
        """
        Метод отправляет первое сообщение и перенаправляет полученное сообщение к методу per_page

        :param message: Последнее сообщение в чате
        """

        msg_text = 'Какое кол-во песен будем выводить?'
        next_msg = self.bot.send_message(chat_id=message.chat.id, text=msg_text)
        self.bot.register_next_step_handler(message=next_msg, callback=self.per_page)

    def per_page(self, message: types.Message) -> None:
        """
        Метод проверяет полученное кол-во песен,
        перенаправляет полученное сообщение к методу save_song_amt

        :param message: Последнее сообщение в чате
        """

        try:
            song_amt = int(message.text)
            if song_amt < 1:
                raise ValueError
            self.save_song_amt(song_amt=song_amt, message=message)

        except ValueError:
            error_msg = 'Введите корректное натуральное число :('
            next_msg = self.bot.send_message(chat_id=message.chat.id, text=error_msg)
            self.bot.register_next_step_handler(message=next_msg, callback=self.per_page)

    def save_song_amt(self, song_amt: int, message: types.Message = None) -> None:
        """
        Метод сохраняет полученное кол-во песен

        :param song_amt: Корректное кол-во песен
        :param message: Последнее сообщение в чате
        """

        self.song_amt = song_amt

    def top_request(self, message: types.Message) -> None:
        """
        Метод делает запрос к api на список песен по заданным фильтрам

        :param message: Последнее сообщение в чате
        """

        url = "https://genius-song-lyrics1.p.rapidapi.com/chart/songs/"
        querystring = {"time_period": self.time_period,
                       "chart_genre": self.genre,
                       "per_page": str(self.song_amt),
                       "page": "1"}

        response = requests.get(url, headers=self._headers, params=querystring)
        song_list = response.json()['chart_items']
        self.create_result(message=message, result_list=song_list)

    def create_result(self, message: types.Message, result_list: List[Dict]) -> None:
        """
        Метод из полученного списка составляет сообщение и отправляет его пользователю

        :param message: Последнее сообщение в чате
        :param result_list: Список с результатами
        """

        top_string = 0
        result_markup = types.InlineKeyboardMarkup()
        result = []

        for song in result_list:
            top_string += 1

            btn_num = types.InlineKeyboardButton(
                text='{num}.'.format(num=top_string),
                callback_data='about_{id}_{user_id}'.format(id=song['item']['id'], user_id=self._user_id)
            )

            result_markup.row(btn_num)

            btn_artist = types.InlineKeyboardButton(
                text='{artist}'.format(artist=song['item']['primary_artist']['name']),
                callback_data='artist_{id}_{user_id}'.format(id=song['item']['primary_artist']['id'],
                                                             user_id=self._user_id)
            )
            btn_song = types.InlineKeyboardButton(
                text='{song}'.format(song=song['item']['title_with_featured']),
                callback_data='about_{id}_{user_id}'.format(id=song['item']['id'], user_id=self._user_id)
            )

            result.append(song['item']['full_title'])
            result_markup.row(btn_artist, btn_song)

        self._result = ';\n'.join(result).replace('"', '""')
        msg = 'Твой топ-{top_amt} песен:\n\n'.format(top_amt=self.song_amt)
        self.bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=result_markup)
        self._save_history()
