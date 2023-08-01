import requests
import random

from .classes import FindCmd
from telebot import types, TeleBot

from typing import List, Dict


class FindSongCmd(FindCmd):
    """
    Класс для поиска песен, если ID песни неизвестен
    (Родитель FindCmd)
    """

    _cmd = 'about'

    def __init__(self, bot: TeleBot, message: types.Message, user_id: int = None) -> None:
        super().__init__(bot=bot, message=message, user_id=user_id)
        self.start_cmd_for_no_id(message=message, start_msg='Введи название песни, которую ты ищешь:')

    def find_list(self, message: types.Message, page: int = 1) -> None:
        """
        Метод формирует список песен и отправляет пользователю

        :param message: Последнее сообщение в чате
        :param page: Номер страницы
        """

        response = super(FindSongCmd, self).find_list(message=message, page=page)
        song_list = response['sections'][1]['hits']
        song_markup, msg_text = self._create_markup_for_song_list(find_list=song_list, page=page)
        self.bot.send_message(chat_id=message.chat.id, text=msg_text, reply_markup=song_markup)
        self._save_history()

    def _create_markup_for_song_list(self, find_list: List[Dict], page: int) -> (types.InlineKeyboardMarkup, str):
        """
        Формирует список песен в виде клавиатуры с ссылками

        :param find_list: Полученный список песен
        :param page: Номер страницы

        :return markup: Клавиатура со списком песен
        :return msg_text: Сообщение для последующей отправки с клавиатурой
        """

        msg_text = ''
        markup = types.InlineKeyboardMarkup()
        top_num = 1 + (5 * (page - 1))

        if len(find_list) != 0:

            result = []
            for obj in find_list:
                btn_song = types.InlineKeyboardButton(
                    text='{num}. {title}'.format(num=top_num, title=obj['result']['full_title']),
                    callback_data='{cmd}_{song_id}_{user_id}'.format(cmd=self._cmd,
                                                                     song_id=obj['result']['id'],
                                                                     user_id=self._user_id)
                )
                markup.add(btn_song)
                top_num += 1
                result.append(obj['result']['full_title'])
            self._result = ';/n'.join(result).replace('"', '""')

            if len(find_list) == 5:
                btn_next = types.InlineKeyboardButton(
                    text='Следующая страница ➡️',
                    callback_data='nextsong_{page}'.format(page=page)
                )
                markup.add(btn_next)

            msg_text = 'Вот все, что я смог найти по-твоему запросу.\n' \
                       'Выбери, какую именно песню будем искать:'

        elif page == 1:
            btn_nth = types.InlineKeyboardButton(
                text='Попробовать ввести заново ➡️',
                callback_data='{cmd}_again_{user_id}'.format(cmd=self._cmd, user_id=self._user_id)
            )
            markup.add(btn_nth)
            self._result = msg_text = 'К сожалению, ничего не удалось найти :('

        if page != 1:
            btn_prev = types.InlineKeyboardButton(
                text='Предыдующая страница ⬅️',
                callback_data='prevsong_{page}'.format(page=page)
            )
            markup.add(btn_prev)

        return markup, msg_text


class FindLyricsCmd(FindSongCmd):
    """
    Класс для поиска песен для команды lyrics без ID песни
    (Родитель FindSongCmd)
    """

    _cmd = 'lyrics'

    def __init__(self, bot: TeleBot, message: types.Message, user_id: int = None) -> None:
        super(FindLyricsCmd, self).__init__(bot=bot, message=message, user_id=user_id)


class FindArtistCmd(FindCmd):
    """
    Класс для поиска исполнителя без ID артиста
    (Родитель FindCmd)
    """

    _cmd = 'artist'

    def __init__(self, bot: TeleBot, message: types.Message, user_id: int = None) -> None:
        super().__init__(bot=bot, message=message, user_id=user_id)
        self.start_cmd_for_no_id(message=message, start_msg='Введи имя исполнителя, которого ты ищешь:')

    def find_list(self, message: types.Message, page: int = 1) -> None:
        """
        Метод формирует список исполнителей и отправляет пользователю

        :param message: Последнее сообщение в чате
        :param page: Номер страницы
        """

        response = super(FindArtistCmd, self).find_list(message=message, page=page)
        artist_list = response['sections'][3]['hits']
        artist_markup, msg_text = self._create_markup_for_artist_list(find_list=artist_list, page=page)
        self.bot.send_message(chat_id=message.chat.id, text=msg_text, reply_markup=artist_markup)
        self._save_history()

    def _create_markup_for_artist_list(self, find_list: List[Dict], page: int) -> (types.InlineKeyboardMarkup, str):
        """
        Формирует список исполнителей в виде клавиатуры с ссылками

        :param find_list: Полученный список исполнителей
        :param page: Номер страницы

        :return markup: Клавиатура со списком исполнителей
        :return msg_text: Сообщение для последующей отправки с клавиатурой
        """

        msg_text = ''
        markup = types.InlineKeyboardMarkup()
        top_num = 1 + (5 * (page - 1))

        if len(find_list) != 0:

            result = []
            for obj in find_list:
                btn_artist = types.InlineKeyboardButton(
                    text='{num}. {artist}'.format(num=top_num, artist=obj['result']['name']),
                    callback_data='artist_{artist_id}_{user_id}'.format(artist_id=obj['result']['id'],
                                                                        user_id=self._user_id)
                )
                markup.add(btn_artist)
                top_num += 1
                result.append(obj['result']['name'])
            self._result = ';\n'.join(result).replace('"', '""')

            if len(find_list) == 5:
                btn_next = types.InlineKeyboardButton(
                    text='Следующая страница ➡️',
                    callback_data='nextartist_{page}'.format(page=page)
                )
                markup.add(btn_next)

            msg_text = 'Вот все, что я смог найти по-твоему запросу.\n' \
                       'Выбери, какого исполнителя именно будем искать:'

        elif page == 1:
            btn_nth = types.InlineKeyboardButton(
                text='Попробовать ввести заново ➡️',
                callback_data='artist_again_{user_id}'.format(user_id=self._user_id)
            )
            markup.add(btn_nth)
            self._result = msg_text = 'К сожалению, ничего не удалось найти :('

        if page != 1:
            btn_prev = types.InlineKeyboardButton(
                text='Предыдующая страница ⬅️',
                callback_data='prevartist_{page}'.format(page=page)
            )
            markup.add(btn_prev)

        return markup, msg_text


class FindSongInfoCmd(FindCmd):
    """
    Класс для поиска песни по ID
    (Родитель FindCmd)

    Attributes:
        id (int): ID искомой песни
    """

    _cmd = 'about'

    def __init__(self, bot: TeleBot, message: types.Message, song_id: int, user_id: int = None) -> None:
        super().__init__(bot=bot, message=message, user_id=user_id)
        self.id = song_id
        self._song_request(message=message)

    def _song_request(self, message: types.Message) -> None:
        """
        Метод делает запрос к api с id песни

        :param message: Последнее сообщение в чате
        """

        url = "https://genius-song-lyrics1.p.rapidapi.com/song/details/"
        querystring = {"id": str(self.id)}
        song_info = requests.get(url, headers=self._headers, params=querystring).json()['song']
        self._create_result_song(info=song_info, message=message)

    def _create_result_song(self, message: types.Message, info: Dict) -> None:
        """
        Метод из полученного словаря формирует результат в сообщение и отправляет его пользователю

        :param message: Последнее сообщение в чате
        :param info: Словарь с информацией о песне
        """

        message_strings = list()
        extra_info_markup = types.InlineKeyboardMarkup()

        message_strings.append('Название: {title}'.format(title=info['title']))
        message_strings.append('Исполнитель: {artist} '.format(artist=info['primary_artist']['name']))

        extra_info_markup.add(types.InlineKeyboardButton(
            text='{artist} ➡️'.format(artist=info['primary_artist']['name']),
            callback_data='artist_{artist_id}_{user_id}'.format(artist_id=info['primary_artist']['id'],
                                                                user_id=self._user_id)
        ))

        if len(info['featured_artists']) > 0:
            feat_artists = []

            for artist in info['featured_artists']:
                feat_artists.append(artist['name'])

                extra_info_markup.add(types.InlineKeyboardButton(
                    text='{artist} ➡️'.format(artist=artist['name']),
                    callback_data='artist_{artist_id}_{user_id}'.format(artist_id=artist['id'], user_id=self._user_id)
                ))

            message_strings[1] += '(Ft. ' + ', '.join(feat_artists) + ')'

        if info['release_date']:
            message_strings.append('Дата релиза: {date}'.format(date=info['release_date']))
        if info['album']:
            message_strings.append('Альбом: {album}'.format(album=info['album']['name']))
        if info['youtube_url']:
            message_strings.append('\n[Посмотреть клип]({video_url})'.format(video_url=info['youtube_url']))

        extra_info_markup.add(types.InlineKeyboardButton(
            text='Текст песни ➡️',
            callback_data='lyrics_{song_id}_{user_id}'.format(song_id=self.id, user_id=self._user_id)
        ))

        self._result = info['full_title'].replace('"', '""')
        msg = '\n'.join(message_strings)
        next_msg = self.bot.send_photo(chat_id=message.chat.id, photo=info['header_image_url'])
        self.bot.send_message(chat_id=next_msg.chat.id, text=msg, reply_markup=extra_info_markup, parse_mode='Markdown')
        self._save_history()


class FindRandomSongCmd(FindSongInfoCmd):
    """
    Класс для команды random, поиск рандомной песни
    (Родитель FindSongInfoCmd)
    """

    _cmd = 'random'

    def __init__(self, bot: TeleBot, message: types.Message) -> None:
        """
        Рандомно подбирается id, удовлетворяющее проверке
        """
        while True:
            random_id = random.randint(1, 9999999)
            if self._test_id(random_id=random_id):
                break
        super(FindRandomSongCmd, self).__init__(bot=bot, message=message, song_id=random_id)

    def _test_id(self, random_id: int) -> bool:
        """
        Проверка на нахождение песни под рандомным id, если песня есть, возвращает True

        :param random_id: id, переданный на проверку
        """

        url = "https://genius-song-lyrics1.p.rapidapi.com/song/details/"
        querystring = {"id": str(random_id)}
        song_info = requests.get(url, headers=self._headers, params=querystring).json()
        if 'error' in song_info.keys():
            return False
        return True


class FindLyricsInfoCmd(FindCmd):
    """
    Класс для команды /lyrics по id
    (Родитель FindCmd)

    Attributes:
        id (int): id песни для поиска ее текста
    """

    _cmd = 'lyrics'

    def __init__(self, bot: TeleBot, message: types.Message, song_id: int, user_id: int) -> None:
        super().__init__(bot=bot, message=message, user_id=user_id)
        self.id = song_id
        self._lyrics_request(message=message)

    def _lyrics_request(self, message: types.Message) -> None:
        """
        Запрос к api на получение текста песни

        :param message: Последнее сообщение в чате
        """

        url = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"
        querystring = {"id": str(self.id), "text_format": "plain"}
        lyrics_info = requests.get(url, headers=self._headers, params=querystring).json()['lyrics']
        self._create_result_lyrics(message=message, info=lyrics_info)

    def _create_result_lyrics(self, message: types.Message, info: Dict) -> None:
        """
        Метод из полученного словаря формирует результат в сообщение и отправляет его пользователю

        :param message: Последнее сообщение в чате
        :param info: Словарь с информацией о песне
        """

        msg_text = 'Песня: {song}\n' \
                   'Исполнитель: {artist}\n\n'.format(song=info['tracking_data']['title'],
                                                      artist=info['tracking_data']['primary_artist'])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            text='О песне ➡️',
            callback_data='about_{song_id}_{user_id}'.format(song_id=self.id, user_id=self._user_id)
        ))
        lyrics = msg_text + info['lyrics']['body']['plain']

        self._result = info['tracking_data']['title'].replace('"', '""')
        self.bot.send_message(chat_id=message.chat.id, text=lyrics, reply_markup=markup)
        self._save_history()


class FindArtistInfoCmd(FindCmd):
    """
    Класс для команды /artist с полученным id, поиск исполнителя

    Attributes:
        id (str): id исполнителя
    """
    _cmd = 'artist'

    def __init__(self, bot: TeleBot, message: types.Message, artist_id: int, user_id: int) -> None:
        super().__init__(bot=bot, message=message, user_id=user_id)
        self.id = artist_id
        self._artist_request(message=message)

    def _artist_request(self, message: types.Message) -> None:
        """
        Запрос к api на получение информации об исполнителе и о его песнях

        :param message: Последнее сообщение в чате
        """

        url = "https://genius-song-lyrics1.p.rapidapi.com/artist/details/"
        querystring = {"id": str(self.id)}
        artist_info = requests.get(url, headers=self._headers, params=querystring).json()['artist']

        url = "https://genius-song-lyrics1.p.rapidapi.com/artist/songs/"
        querystring = {"id": str(self.id), "sort": "popularity", "per_page": "10", "page": "1"}
        artist_songs = requests.get(url, headers=self._headers, params=querystring).json()['songs']

        self._create_result_artist(info=artist_info, songs=artist_songs, message=message)

    def _create_result_artist(self, info: Dict, songs: List[Dict], message: types.Message) -> None:
        """
        Метод из полученного словаря формирует результат в сообщение и отправляет его пользователю

        :param message: Последнее сообщение в чате
        :param songs: Список песней исполнителя
        :param info: Словарь с информацией о песне
        """

        songs_markup = types.InlineKeyboardMarkup()
        top_num = 0

        msg_text = 'Исполнитель: {artist_name}\n' \
                   'Самые популярные работы:'.format(artist_name=info['name'])
        for song in songs:
            top_num += 1
            btn_song = types.InlineKeyboardButton(
                text='{num}. {song_title}'.format(num=top_num, song_title=song['title_with_featured']),
                callback_data='about_{song_id}_{user_id}'.format(song_id=song['id'], user_id=self._user_id)
            )
            songs_markup.add(btn_song)

        self._result = info['name'].replace('"', '""')
        photo_send = self.bot.send_photo(chat_id=message.chat.id, photo=info['image_url'])
        self.bot.send_message(chat_id=photo_send.chat.id, text=msg_text, reply_markup=songs_markup)
        self._save_history()
