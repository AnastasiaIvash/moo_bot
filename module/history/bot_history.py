
from telebot import TeleBot, types
from .model_class import DB as db, User, Command


class ShowHistoryCmd:
    """
    Класс, формирующий запрос к БД на получение истории последних запросов
    """

    def __init__(self, bot: TeleBot, message: types.Message) -> None:
        self.bot = bot
        self._user_id = message.from_user.id
        self._history_request(message=message)

    def _history_request(self, message: types.Message) -> None:
        """
        Метод делает запрос к БД по ID пользователя, получив ответ, оформляет сообщение и отправляет его

        :param message: Последнее сообщение в чате
        """
        with db:
            db.create_tables([User, Command])

            get_user = User.get_or_create(user_id=self._user_id)[0]
            cmd_list = Command.select().where(Command.user == get_user)
            if cmd_list:
                msg_strings = []
                for command in cmd_list:
                    msg_strings.append('Команда: /{cmd_name}\n'
                                       'Дата запроса: {create}\n'
                                       'Результ: \n{res}\n'.format(cmd_name=command.cmd_name,
                                                                   create=command.created_at,
                                                                   res=command.result))
                    msg_text = 'Вот твоя история поиска:\n\n' + '\n'.join(msg_strings)

            else:
                msg_text = 'Ты еще не пробовал ни одну комманду.\n' \
                           'Если тебе интересно, на какие команды я откликаюсь, ' \
                           'воспользуйся /help!'

            self.bot.send_message(chat_id=message.chat.id, text=msg_text)
