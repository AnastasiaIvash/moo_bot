
import telebot

from backoff_utils import apply_backoff, strategies
from module.texts import text_response, start, help
from module.history.bot_history import ShowHistoryCmd
from module.find_list_class import FindTopListCmd, FindTopCustomListCmd
from module.find_class import FindSongCmd, FindSongInfoCmd, \
    FindArtistCmd, FindArtistInfoCmd, FindLyricsCmd, \
    FindLyricsInfoCmd, FindRandomSongCmd

BOT_NAME = 'MoovieBot'
BOT_URL = 'https://web.telegram.org/k/#@CowMoovieBot'

with open('bot_token.txt', 'r') as file:
    BOT_TOKEN = str(file.readline())

moo_bot = telebot.TeleBot(BOT_TOKEN)
# api - https://rapidapi.com/Glavier/api/genius-song-lyrics1


# top


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['top'])
def top_command(message: telebot.types.Message):
    global cmd
    cmd = FindTopListCmd(bot=moo_bot, message=message)

# top_custom


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['top_custom'])
def top_custom_command(message: telebot.types.Message):
    global cmd
    cmd = FindTopCustomListCmd(bot=moo_bot, message=message)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data in ['day', 'week', 'month', 'all_time'])
def period_callback(call: telebot.types.CallbackQuery):
    global cmd
    cmd.time_period = call.data
    cmd.genre_keyboard(call.message)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data in ['rap', 'pop', 'rb', 'rock', 'country', 'all'])
def genre_callback(call: telebot.types.CallbackQuery):
    global cmd
    cmd.genre = call.data
    cmd.top_request(message=call.message)


# about


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['about'])
def about_command(message):
    global cmd
    cmd = FindSongCmd(bot=moo_bot, message=message)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('nextsong_'))
def about_next_page(call: telebot.types.CallbackQuery):
    global cmd
    page = int(call.data.split('_')[1]) + 1
    cmd.find_list(message=call.message, page=page)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('prevsong_'))
def about_prev_page(call: telebot.types.CallbackQuery):
    global cmd
    page = int(call.data.split('_')[1]) - 1
    cmd.find_list(message=call.message, page=page)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data == 'about_again')
def about_again(call: telebot.types.CallbackQuery):
    global cmd
    user_id = int(call.data.split('_')[2])
    cmd = FindSongCmd(bot=moo_bot, message=call.message, user_id=user_id)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('about_'))
def about_command_with_id(call: telebot.types.CallbackQuery):
    global cmd
    song_id = int(call.data.split('_')[1])
    user_id = int(call.data.split('_')[2])
    cmd = FindSongInfoCmd(bot=moo_bot, message=call.message, song_id=song_id, user_id=user_id)

# artist


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['artist'])
def artist_command(message: telebot.types.Message):
    global cmd
    cmd = FindArtistCmd(bot=moo_bot, message=message)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('nextartist_'))
def artist_next_page(call: telebot.types.CallbackQuery):
    global cmd
    page = int(call.data.split('_')[1]) + 1
    cmd.find_list(message=call.message, page=page)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('prevartist_'))
def artist_next_page(call: telebot.types.CallbackQuery):
    global cmd
    page = int(call.data.split('_')[1]) - 1
    cmd.find_list(message=call.message, page=page)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data == 'artist_again')
def artist_again(call: telebot.types.CallbackQuery):
    global cmd
    user_id = int(call.data.split('_')[2])
    cmd = FindArtistCmd(bot=moo_bot, message=call.message, user_id=user_id)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('artist_'))
def artist_command_with_id(call: telebot.types.CallbackQuery):
    global cmd
    artist_id = int(call.data.split('_')[1])
    user_id = int(call.data.split('_')[2])
    cmd = FindArtistInfoCmd(bot=moo_bot, message=call.message, artist_id=artist_id, user_id=user_id)

# lyrics


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['lyrics'])
def lyrics_command(message):
    global cmd
    cmd = FindLyricsCmd(bot=moo_bot, message=message)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('nextsong_'))
def lyrics_next_page(call: telebot.types.CallbackQuery):
    global cmd
    page = int(call.data.split('_')[1]) + 1
    cmd.find_list(message=call.message, page=page)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('prevsong_'))
def lyrics_prev_page(call: telebot.types.CallbackQuery):
    global cmd
    page = int(call.data.split('_')[1]) - 1
    cmd.find_list(message=call.message, page=page)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data == 'lyrics_again')
def lyrics_again(call: telebot.types.CallbackQuery):
    global cmd
    user_id = int(call.data.split('_')[2])
    cmd = FindLyricsCmd(bot=moo_bot, message=call.message, user_id=user_id)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.callback_query_handler(func=lambda call: call.data.startswith('lyrics_'))
def lyrics_command_with_id(call: telebot.types.CallbackQuery):
    global cmd
    song_id = int(call.data.split('_')[1])
    user_id = int(call.data.split('_')[2])
    cmd = FindLyricsInfoCmd(bot=moo_bot, message=call.message,
                            song_id=song_id, user_id=user_id)

# random


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['random'])
def random_command(message: telebot.types.Message):
    global cmd
    cmd = FindRandomSongCmd(bot=moo_bot, message=message)

# history


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['history'])
def history_command(message: telebot.types.Message):
    global cmd
    cmd = ShowHistoryCmd(bot=moo_bot, message=message)

# texts


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['start'])
def start_command(message):
    start(moo_bot, message)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(commands=['help'])
def help_command(message):
    help(moo_bot, message)


@apply_backoff(strategies.Exponential, max_tries=5, max_delay=30)
@moo_bot.message_handler(content_types=['text'])
def text_message(message):
    text_response(moo_bot, message)

# end


moo_bot.infinity_polling()
