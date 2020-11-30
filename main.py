from telebot import types
import telebot
import time
import re
import threading

token = "1427693199:AAGnuGWcgwUy5tLlE7_GKyomLCHKY_T5mZI"
bot = telebot.TeleBot(token=token)

users = []
chats = []


class UserInBot:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__can_change = False
        self.__can_change_words = False
        self.__can_change_links = False
        self.__can_change_names = False
        self.__can_del_button = False
        self.__can_change_time_banned = False
        self.__can_change_group_banned = False
        self.__can_change_friend_banned = False
        self.__number_chat = 0

    def get_user_id(self):
        return self.__user_id

    def get_can_change(self):
        return self.__can_change

    def set_can_change(self, can_change):
        self.__can_change = can_change

    def get_can_change_words(self):
        return self.__can_change_words

    def set_can_change_words(self, can_change_words):
        self.__can_change_words = can_change_words

    def get_can_change_time_banned(self):
        return self.__can_change_time_banned

    def set_can_change_time_banned(self, can_change_time_banned):
        self.__can_change_time_banned = can_change_time_banned

    def get_can_change_group_banned(self):
        return self.__can_change_group_banned

    def set_can_change_group_banned(self, can_change_group_banned):
        self.__can_change_group_banned = can_change_group_banned

    def get_can_change_friend_banned(self):
        return self.__can_change_friend_banned

    def set_can_change_friend_banned(self, can_change_friend_banned):
        self.__can_change_friend_banned = can_change_friend_banned

    def get_can_change_links(self):
        return self.__can_change_links

    def set_can_change_links(self, can_change_links):
        self.__can_change_links = can_change_links

    def get_can_change_names(self):
        return self.__can_change_names

    def set_can_change_names(self, can_change_names):
        self.__can_change_names = can_change_names

    def get_can_del_button(self):
        return self.__can_del_button

    def set_can_del_button(self, can_del_button):
        self.__can_del_button = can_del_button

    def get_number_chat(self):
        return self.__number_chat

    def set_number_chat(self, number_chat):
        self.__number_chat = number_chat


class UserInChat:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__time_of_ban = 0
        self.__when_banned = 0
        self.__is_time_banned = False
        self.__is_group_banned = False
        self.__is_friend_banned = False
        self.__is_banned = False
        self.__friends_count = 0
        self.__invited_friends = []

    def get_user_id(self):
        return self.__user_id

    def get_time_of_ban(self):
        return self.__time_of_ban

    def set_time_of_ban(self, time_of_ban):
        self.__time_of_ban = time_of_ban

    def get_when_banned(self):
        return self.__when_banned

    def set_when_banned(self, when_banned):
        self.__when_banned = when_banned

    def set_is_time_banned(self, is_time_banned):
        self.__is_time_banned = is_time_banned

    def get_is_time_banned(self):
        return self.__is_time_banned

    def set_is_group_banned(self, is_group_banned):
        self.__is_group_banned = is_group_banned

    def get_is_group_banned(self):
        return self.__is_group_banned

    def set_is_friend_banned(self, is_friend_banned):
        self.__is_friend_banned = is_friend_banned

    def get_is_friend_banned(self):
        return self.__is_friend_banned

    def set_is_banned(self, is_banned):
        self.__is_banned = is_banned

    def get_is_banned(self):
        return self.__is_banned

    def set_friends_count(self, friends_count):
        self.__friends_count = friends_count

    def get_friends_count(self):
        return self.__friends_count

    def add_invited_friends(self, friend):
        self.__invited_friends.append(friend)

    def get_invited_friends(self):
        return self.__invited_friends


class Chat:
    def __init__(self, owner_id, chat_id):
        self.__owner_id = owner_id
        self.__chat_id = chat_id
        self.__banned_words = []
        self.__button_links = []
        self.__button_names = []
        self.__links = True
        self.__forward = True
        self.__welcome = False
        self.__buttons_new = False
        self.__buttons_time = False
        self.__banned_time = 0
        self.__banned_chanel = 0
        self.__banned_chanel_name = ""
        self.__banned_chanel_all = 0
        self.__banned_chanel_new = 0
        self.__banned_friend = 0
        self.__banned_friend_one = 0
        self.__banned_friend_every = 0
        self.__users_in_chat = []
        self.__new_users_in_chat = []

    def get_owner_id(self):
        return self.__owner_id

    def get_chat_id(self):
        return self.__chat_id

    def set_banned_words(self, banned_words):
        self.__banned_words = banned_words

    def get_banned_words(self):
        return self.__banned_words

    def get_links(self):
        return self.__links

    def change_links(self):
        self.__links = not self.__links

    def get_forward(self):
        return self.__forward

    def change_forward(self):
        self.__forward = not self.__forward

    def get_welcome(self):
        return self.__welcome

    def change_welcome(self):
        self.__welcome = not self.__welcome

    def get_buttons_new(self):
        return self.__buttons_new

    def change_buttons_new(self):
        self.__buttons_new = not self.__buttons_new

    def get_buttons_time(self):
        return self.__buttons_time

    def change_buttons_time(self):
        self.__buttons_time = not self.__buttons_time

    def get_users_in_chat(self):
        return self.__users_in_chat

    def set_users_in_chat(self, users_in_chat):
        self.__users_in_chat = users_in_chat

    def add_user_in_chat(self, user_id):
        self.__users_in_chat.append(UserInChat(user_id))

    def is_user_in_chat(self, user_id):
        for us in self.__users_in_chat:
            if us.get_user_id() == user_id:
                return True
        return False

    def get_button_links(self):
        return self.__button_links

    def set_button_links(self, button_links):
        self.__button_links = button_links

    def add_button_links(self, link):
        self.__button_links.append(link)

    def get_button_names(self):
        return self.__button_names

    def set_button_names(self, button_names):
        self.__button_names = button_names

    def add_button_names(self, name):
        self.__button_names.append(name)

    def add_new_user_in_chat(self, user_id):
        self.__new_users_in_chat.append(user_id)

    def is_new_user_in_chat(self, user_id):
        return user_id in self.__new_users_in_chat

    def get_banned_time(self):
        return self.__banned_time

    def set_banned_time(self, banned_time):
        self.__banned_time = banned_time

    def get_banned_chanel(self):
        return self.__banned_chanel

    def set_banned_chanel(self, banned_chanel):
        self.__banned_chanel = banned_chanel

    def get_banned_chanel_name(self):
        return self.__banned_chanel_name

    def set_banned_chanel_name(self, banned_chanel_name):
        self.__banned_chanel_name = banned_chanel_name

    def get_banned_chanel_all(self):
        return self.__banned_chanel_all

    def set_banned_chanel_all(self, banned_chanel_all):
        self.__banned_chanel_all = banned_chanel_all

    def get_banned_chanel_new(self):
        return self.__banned_chanel_new

    def set_banned_chanel_new(self, banned_chanel_new):
        self.__banned_chanel_new = banned_chanel_new

    def get_banned_friend_one(self):
        return self.__banned_friend_one

    def set_banned_friend_one(self, banned_friend_one):
        self.__banned_friend_one = banned_friend_one

    def get_banned_friend_every(self):
        return self.__banned_friend_every

    def set_banned_friend_every(self, banned_friend_every):
        self.__banned_friend_every = banned_friend_every

    def get_banned_friend(self):
        return self.__banned_friend

    def set_banned_friend(self, banned_friend):
        self.__banned_friend = banned_friend


def is_user(user_id):
    for us in users:
        if user_id == us.get_user_id():
            return True
    return False


def is_chat(chat_id):
    for chat in chats:
        if chat_id == chat.get_chat_id():
            return True
    return False


def get_user(user_id):
    counter = 0
    for us in users:
        if us.get_user_id() == user_id:
            return counter
        counter += 1


def get_chat(chat_id):
    chat_numb = 0
    for chat in chats:
        if chat.get_chat_id() == chat_id:
            return chat_numb
        chat_numb += 1


def chat_number(user_id):
    for us in users:
        if us.get_user_id() == user_id:
            chat_numb = us.get_number_chat()

    names = 0
    counter = -1
    for chat in chats:
        if chat_numb == names:
            return counter
        if chat.get_owner_id() == user_id:
            names += 1
        counter += 1
    if chat_numb == names:
        return counter


def start_buttons():
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Новости", callback_data="news")
    but_2 = types.InlineKeyboardButton(text="Поддержка", url="https://t.me/N0tdefined")
    but_3 = types.InlineKeyboardButton(text="Настройка чатов", callback_data="my_chats")
    but_4 = types.InlineKeyboardButton(text="Как пользоваться", callback_data="info")
    key.add(but_1, but_2)
    key.add(but_3, but_4)
    return key


def settings_buttons(chat_numb):
    if chats[chat_numb].get_links():
        link_txt = "(разрешены)"
    else:
        link_txt = "(запрещены)"

    if chats[chat_numb].get_forward():
        forward_txt = "(разрешены)"
    else:
        forward_txt = "(запрещены)"

    if chats[chat_numb].get_welcome():
        welcome_txt = "(включено)"
    else:
        welcome_txt = "(выключено)"



    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Запрещённые слова", callback_data="banned_words")
    but_2 = types.InlineKeyboardButton(text="Ссылки" + link_txt, callback_data="url")
    but_3 = types.InlineKeyboardButton(text="Пересланные сообщения" + forward_txt, callback_data="forwarded")
    but_4 = types.InlineKeyboardButton(text="Запреты писать", callback_data="banned_user")
    but_5 = types.InlineKeyboardButton(text="Приветствие"+welcome_txt, callback_data="welcome")
    but_6 = types.InlineKeyboardButton(text="Кнопки", callback_data="buttons")
    but_7 = types.InlineKeyboardButton(text="Назад", callback_data="start")
    key.add(but_1, but_2)
    key.add(but_3)
    key.add(but_4)
    key.add(but_5)
    key.add(but_6)
    key.add(but_7)
    return key


@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id > 0:
        key = start_buttons()
        if not is_user(message.chat.id):
            name = f"[{message.from_user.first_name}](tg://user?id={str(message.chat.id)})"
            text = f"Добро пожаловать {name}, я бот для модерации чатов. " \
                   f"Помогаю управлять чатами, в том числе удалять спам ссылки," \
                   f" сообщения с нецензурной бранью и многое другое."
            users.append(UserInBot(message.chat.id))
        else:
            text = "Выберите действие"

        bot.send_message(message.chat.id, text, reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "start")
def start(call):
    if call.message.chat.id > 0:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            pass
        key = start_buttons()
        text = "Выберите действие"
        bot.send_message(call.from_user.id, text, reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "news")
def news(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Пока что новостей нет.")
    start(call)


@bot.callback_query_handler(func=lambda call: call.data == "info")
def info(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.from_user.id, "Добавьте бота в свою группу (важно, для это должна быть супергруппа),"
                                        " повысьте его права"
                                        " до администратора, далее создатель чата может"
                                        " настроить бота (Мои чаты -> Настройка чатов)")
    start(call)


@bot.callback_query_handler(func=lambda call: call.data == "my_chats")
def my_chats(call):
    names = []
    for chat in chats:
        if chat.get_owner_id() == call.from_user.id:
            for admin in bot.get_chat_administrators(chat.get_chat_id()):
                if admin.status == "creator" and admin.user.id == call.from_user.id:
                    names.append(bot.get_chat(chat.get_chat_id()).title)

    if not names:
        bot.send_message(call.from_user.id, "У вас нет чатов с ботом")
    else:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            pass
        number = get_user(call.from_user.id)
        users[number].set_can_change(True)
        txt = "Введите номер чата\n"
        for i in range(len(names)):
            txt += names[i] + " - " + str(i + 1) + "\n"
        bot.send_message(call.from_user.id, txt)


@bot.message_handler(commands=[""])
def chat_settings(message):
    if message.chat.id > 0:
        try:
            chat_numb = chat_number(message.chat.id)
            key = settings_buttons(chat_numb)
            bot.send_message(message.chat.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')
        except Exception as e:
            print(e)


@bot.callback_query_handler(func=lambda call: call.data == "chat_settings")
def chat_settings(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    chat_numb = chat_number(call.from_user.id)
    key = settings_buttons(chat_numb)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "banned_words")
def banned_words(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    chat_numb = chat_number(call.from_user.id)
    banned_w = chats[chat_numb].get_banned_words()
    if banned_w:
        bot.send_message(call.from_user.id, "Запрещённые слова: " + " ".join(banned_w))
    else:
        bot.send_message(call.from_user.id, "Запрещённых слов нет")

    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Изменить запрещённые слова", callback_data="change_banned_words")
    but_2 = types.InlineKeyboardButton(text="Назад", callback_data="chat_settings")
    key.add(but_1)
    key.add(but_2)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "change_banned_words")
def change_banned_words(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_change_words(True)
    bot.send_message(call.from_user.id, "Введите запрещённые слова через пробел\nПример: один два три")


@bot.callback_query_handler(func=lambda call: call.data == "url")
def url(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].change_links()
    chat_settings(call)


@bot.callback_query_handler(func=lambda call: call.data == "forwarded")
def forwarded(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].change_forward()
    chat_settings(call)


@bot.callback_query_handler(func=lambda call: call.data == "banned_user")
def banned_user(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    key = types.InlineKeyboardMarkup()
    chat_numb = chat_number(call.from_user.id)
    if chats[chat_numb].get_banned_time() == 0:
        banned_time_txt = "(нет)"
    else:
        banned_time_txt = f"({chats[chat_numb].get_banned_time()} минут)"

    if chats[chat_numb].get_banned_chanel_name() == "":
        banned_chanel_txt = "(нет)"
    else:
        banned_chanel_txt = f"(@{chats[chat_numb].get_banned_chanel_name()})"

    if chats[chat_numb].get_banned_friend() == 0:
        banned_friend_txt = "(нет)"
    else:
        banned_friend_txt = f"({chats[chat_numb].get_banned_friend()} чел.)"
    but_1 = types.InlineKeyboardButton(text="Запрет писать первое время " + banned_time_txt,
                                       callback_data="banned_by_time")

    but_2 = types.InlineKeyboardButton(text="Запрет писать если не в канале " + banned_chanel_txt,
                                       callback_data="banned_by_chanel")

    but_3 = types.InlineKeyboardButton(text="Запрет писать если не добавил друга" + banned_friend_txt,
                                       callback_data="banned_by_friend")

    but_4 = types.InlineKeyboardButton(text="Назад", callback_data="chat_settings")
    key.add(but_1)
    key.add(but_2)
    key.add(but_3)
    key.add(but_4)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "banned_by_time")
def banned_by_time(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    key = types.InlineKeyboardMarkup()
    chat_numb = chat_number(call.from_user.id)
    if chats[chat_numb].get_banned_time() == 0:
        bot.send_message(call.from_user.id, "(Сейчас нет времени запрета писать)")
    else:
        bot.send_message(call.from_user.id, f"(Время запрета писать - {chats[chat_numb].get_banned_time()} минут)")
    but_1 = types.InlineKeyboardButton(text="Изменить время запрета",
                                       callback_data="banned_time_change")

    but_2 = types.InlineKeyboardButton(text="Назад", callback_data="banned_user")
    key.add(but_1)
    key.add(but_2)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "banned_time_change")
def banned_time_change(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_change_time_banned(True)
    bot.send_message(call.from_user.id, "Введите время (в минутах) сколько нельзя писать новым участники группы")


@bot.callback_query_handler(func=lambda call: call.data == "banned_by_chanel")
def banned_by_chanel(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass

    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Применять ко всем участникам", callback_data="banned_chanel_all")
    but_2 = types.InlineKeyboardButton(text="Применять только к новым участникам", callback_data="banned_chanel_new")
    but_3 = types.InlineKeyboardButton(text="Назад", callback_data="banned_user")
    key.add(but_1)
    key.add(but_2)
    key.add(but_3)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "banned_chanel_all")
def banned_chanel_all(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_change_group_banned(True)
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].set_banned_chanel_new(0)
    chats[chat_numb].set_banned_chanel_all(1)
    bot.send_message(call.from_user.id, "Добавьте бота в канал и после этого парешлите "
                                        "боту любой пост с канала где есть текст.")


@bot.callback_query_handler(func=lambda call: call.data == "banned_chanel_new")
def banned_chanel_new(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_change_group_banned(True)
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].set_banned_chanel_new(1)
    chats[chat_numb].set_banned_chanel_all(0)
    bot.send_message(call.from_user.id, "Добавьте бота в канал и после этого парешлите "
                                        "боту любой пост с канала где есть текст.")


@bot.callback_query_handler(func=lambda call: call.data == "banned_by_friend")
def banned_by_friend(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass

    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Применять только один раз", callback_data="banned_friend_one")
    but_2 = types.InlineKeyboardButton(text="Применять для каждого поста", callback_data="banned_friend_every")
    but_3 = types.InlineKeyboardButton(text="Назад", callback_data="banned_user")
    key.add(but_1)
    key.add(but_2)
    key.add(but_3)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "banned_friend_one")
def banned_friend_one(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_change_friend_banned(True)
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].set_banned_friend_one(1)
    chats[chat_numb].set_banned_friend_every(0)
    bot.send_message(call.from_user.id, "Введите количество человек, сколько нужно пригласить.")


@bot.callback_query_handler(func=lambda call: call.data == "banned_friend_every")
def banned_friend_every(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_change_friend_banned(True)
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].set_banned_friend_one(0)
    chats[chat_numb].set_banned_friend_every(1)
    bot.send_message(call.from_user.id, "Введите количество человек, сколько нужно пригласить.")


@bot.callback_query_handler(func=lambda call: call.data == "welcome")
def welcome(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_change_friend_banned(True)
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].set_banned_friend_one(0)
    chats[chat_numb].set_banned_friend_every(1)
    bot.send_message(call.from_user.id, "Введите количество человек, сколько нужно пригласить.")


@bot.callback_query_handler(func=lambda call: call.data == "buttons")
def buttons(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_del_button(False)
    chat_numb = chat_number(call.from_user.id)
    if chats[chat_numb].get_buttons_new():
        buttons_new_txt = "(включено)"
    else:
        buttons_new_txt = "(выключено)"

    if chats[chat_numb].get_buttons_time():
        buttons_time_txt = "(включено)"
    else:
        buttons_time_txt = "(выключено)"

    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Добавить кнопку", callback_data="add_button")
    but_2 = types.InlineKeyboardButton(text="Публиковать для новых игроков"+buttons_new_txt,
                                       callback_data="turn_on_buttons_new")
    but_3 = types.InlineKeyboardButton(text="Публиковать по времени" + buttons_time_txt,
                                       callback_data="turn_on_buttons_time")
    but_4 = types.InlineKeyboardButton(text="Показать кнопки", callback_data="show_buttons")
    but_5 = types.InlineKeyboardButton(text="Удалить кнопку", callback_data="del_button")
    but_6 = types.InlineKeyboardButton(text="Назад", callback_data="chat_settings")

    key.add(but_1)
    key.add(but_2)
    key.add(but_3)
    key.add(but_4)
    key.add(but_5)
    key.add(but_6)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "add_button")
def add_button(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    number = get_user(call.from_user.id)
    users[number].set_can_change_links(True)
    bot.send_message(call.from_user.id, "Пришлите ссылку.")


@bot.callback_query_handler(func=lambda call: call.data == "del_button")
def del_button(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    chat_numb = chat_number(call.from_user.id)
    number = get_user(call.from_user.id)

    names = chats[chat_numb].get_button_names()
    txt = "Введите номер кнопки, которую хотите удалить:\n"

    for i in range(len(names)):
        txt += names[i] + " - " + str(i+1) + "\n"

    if len(names) == 0:
        txt = "Кнопок нет"

    users[number].set_can_del_button(True)

    bot.send_message(call.from_user.id, txt)


@bot.callback_query_handler(func=lambda call: call.data == "show_buttons")
def show_buttons(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    chat_numb = chat_number(call.from_user.id)
    links = chats[chat_numb].get_button_links()
    names = chats[chat_numb].get_button_names()

    keyboard = types.InlineKeyboardMarkup()

    for i in range(len(names)):
        keyboard.add(types.InlineKeyboardButton(text=names[i], url=links[i]))

    if len(names) == 0:
        txt = "Кнопок нет"
    else:
        txt = "Кнопки:"

    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="buttons"))
    bot.send_message(call.from_user.id, txt, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "turn_on_buttons_new")
def turn_on_buttons_new(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].change_buttons_new()
    buttons(call)


@bot.callback_query_handler(func=lambda call: call.data == "turn_on_buttons_time")
def turn_on_buttons_time(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        pass
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].change_buttons_time()
    buttons(call)


@bot.message_handler(content_types=["new_chat_members"])
def new_member(message):
    for admin in bot.get_chat_administrators(message.chat.id):
        if admin.status == "creator" and not is_chat(message.chat.id):
            chats.append(Chat(admin.user.id, message.chat.id))

    chat_numb = get_chat(message.chat.id)
    users_in_chat = chats[chat_numb].get_users_in_chat()

    if message.new_chat_members[0].id != message.from_user.id:
        id_user = message.new_chat_members[0].id
        name = message.new_chat_members[0].first_name
        for us in users_in_chat:
            friends = us.get_invited_friends()
            if us.get_user_id() == message.from_user.id and not (message.new_chat_members[0].id in friends):
                us.set_friends_count(us.get_friends_count() + 1)
                us.add_invited_friends(message.new_chat_members[0].id)
    else:
        id_user = message.from_user.id
        name = message.from_user.first_name

    try:
        chat_numb = get_chat(message.chat.id)
        if not chats[chat_numb].is_user_in_chat(id_user):
            chats[chat_numb].add_user_in_chat(id_user)

        if not chats[chat_numb].is_new_user_in_chat(id_user):
            chats[chat_numb].add_new_user_in_chat(id_user)

        users_in_chat = chats[chat_numb].get_users_in_chat()
        for us in users_in_chat:
            if us.get_user_id() == id_user:
                if chats[chat_numb].get_banned_time() > 0:
                    us.set_time_of_ban(chats[chat_numb].get_banned_time())
                    us.set_when_banned(time.time())
                    us.set_is_time_banned(True)
                    bot.restrict_chat_member(chats[chat_numb].get_chat_id(), us.get_user_id())

                if chats[chat_numb].get_banned_chanel() != 0:
                    try:
                        member = bot.get_chat_member(chats[chat_numb].get_chat_banned(), id_user)
                        if member and str(member.status) != "left":
                            pass
                    except Exception as e:
                        bot.restrict_chat_member(chats[chat_numb].get_chat_id(), us.get_user_id())

                        us.set_is_group_banned(True)

        text = f"Добро пожаловать, {name}"
        bot.send_message(message.chat.id, text)
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=["left_chat_member"])
def left_member(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception:
        pass


def check_banned():
    old_time = time.time()
    while True:
        if time.time() - old_time > 1:
            for chat in chats:
                users_in_chat = chat.get_users_in_chat()
                for us in users_in_chat:
                    if time.time() - us.get_when_banned() > us.get_time_of_ban() * 60 and us.get_is_time_banned():
                        us.set_is_time_banned(False)

                    try:
                        member = bot.get_chat_member(chat.get_banned_chanel(), us.get_user_id())
                        if chat.get_banned_chanel() != 0:
                            if chat.get_banned_chanel_all() == 1:
                                if member and str(member.status) == "left":
                                    us.set_is_group_banned(True)
                                else:
                                    us.set_is_group_banned(False)

                            elif chat.get_banned_chanel_new() == 1 and chat.is_new_user_in_chat(us.get_user_id()):
                                if member and str(member.status) == "left":
                                    us.set_is_group_banned(True)
                                else:
                                    us.set_is_group_banned(False)
                    except Exception as e:
                        pass
                    if chat.get_banned_friend() != 0:
                        if us.get_friends_count() >= chat.get_banned_friend():
                            us.set_is_friend_banned(False)
                        else:
                            us.set_is_friend_banned(True)

                    try:
                        if not us.get_is_time_banned() and not us.get_is_group_banned() and not us.get_is_friend_banned():
                            if us.get_is_banned():
                                bot.promote_chat_member(chat.get_chat_id(), us.get_user_id())
                                us.set_is_banned(False)
                        else:
                            if not us.get_is_banned():
                                bot.restrict_chat_member(chat.get_chat_id(), us.get_user_id())
                                us.set_is_banned(True)

                    except Exception as e:
                        pass

            old_time = time.time()


@bot.message_handler()
def message_handler(message):
    if message.chat.id > 0:
        names = []
        for chat in chats:
            if chat.get_owner_id() == message.chat.id:
                names.append(bot.get_chat(chat.get_chat_id()).title)

        is_any = False
        chat_numb = chat_number(message.chat.id)
        amount_buttons = len(chats[chat_numb].get_button_names())
        for us in users:
            if us.get_user_id() == message.chat.id and us.get_can_change():
                is_any = True
                if message.text.isdigit():
                    if 0 < int(message.text) <= len(names):
                        us.set_number_chat(int(message.text))
                        us.set_can_change(False)
                        chat_settings(message)
                    else:
                        bot.send_message(message.chat.id, "Такого номера чата нет.")
                else:
                    bot.send_message(message.chat.id, "Некорректный ввод.")
            elif us.get_user_id() == message.chat.id and us.get_can_change_words():
                is_any = True
                words = message.text
                words = words.split(" ")
                chats[chat_numb].set_banned_words(words)
                us.set_can_change_words(False)
                chat_settings(message)
            elif us.get_user_id() == message.chat.id and us.get_can_change_time_banned():
                is_any = True
                if message.text.isdigit():
                    if 0 < int(message.text) <= 10080:
                        chats[chat_numb].set_banned_time(int(message.text))
                        us.set_can_change_time_banned(False)
                        banned_user(message)
                    else:
                        bot.send_message(message.chat.id, "Число должно быть в диапазоне 0-10080")
                else:
                    bot.send_message(message.chat.id, "Некорректный ввод.")

            elif us.get_user_id() == message.chat.id and us.get_can_change_group_banned():
                if message.forward_from_chat:
                    try:
                        bot.get_chat_member(message.forward_from_chat.id, us.get_user_id())
                        chats[chat_numb].set_banned_chanel(message.forward_from_chat.id)
                        chats[chat_numb].set_banned_chanel_name(message.forward_from_chat.username)
                        us.set_can_change_group_banned(False)
                        is_any = True
                        banned_user(message)
                    except Exception:
                        bot.send_message(message.chat.id, "Сперва добавьте бота в канал.")
                        is_any = True
            elif us.get_user_id() == message.chat.id and us.get_can_change_friend_banned():
                is_any = True
                if message.text.isdigit():
                    if 0 < int(message.text) <= 30:
                        chats[chat_numb].set_banned_friend(int(message.text))
                        us.set_can_change_friend_banned(False)
                        banned_user(message)
                    else:
                        bot.send_message(message.chat.id, "Число должно быть в диапазоне 0-30")
                else:
                    bot.send_message(message.chat.id, "Некорректный ввод.")

            elif us.get_user_id() == message.chat.id and us.get_can_change_links():
                is_any = True
                text_lst = message.text.split(" ")
                if re.search(r'\bhttps://\b', message.text) and len(text_lst) == 1:
                    us.set_can_change_links(False)
                    us.set_can_change_names(True)
                    chats[chat_numb].add_button_links(message.text)

                    bot.send_message(message.chat.id, "Теперь напишите название кнопки")
                else:
                    bot.send_message(message.chat.id, "Некорректный ввод.")

            elif us.get_user_id() == message.chat.id and us.get_can_change_names():
                is_any = True
                us.set_can_change_names(False)
                chats[chat_numb].add_button_names(message.text)
                chat_settings(message)
            elif us.get_user_id() == message.chat.id and us.get_can_del_button():
                is_any = True
                if message.text.isdigit():
                    if 0 < int(message.text) <= amount_buttons:
                        try:
                            links_but = chats[chat_numb].get_button_links()
                            names_but = chats[chat_numb].get_button_names()
                            links_but.__delitem__(int(message.text) - 1)
                            names_but.__delitem__(int(message.text) - 1)
                            chats[chat_numb].set_button_links(links_but)
                            chats[chat_numb].set_button_names(names_but)
                        except Exception as e:
                            print(e)

                        us.set_can_del_button(False)
                        buttons(message)
                    else:
                        bot.send_message(message.chat.id, "Такой кнопки нет.")
                else:
                    bot.send_message(message.chat.id, "Некорректный ввод.")

        if not is_any:
            bot.send_message(message.chat.id, "Извините, я не понял.")
    else:
        try:
            admins = []
            for admin in bot.get_chat_administrators(message.chat.id):
                admins.append(admin.user.id)
                if admin.status == "creator" and not is_chat(message.chat.id):
                    chats.append(Chat(admin.user.id, message.chat.id))
            chat_numb = get_chat(message.chat.id)
            users_in_chat = chats[chat_numb].get_users_in_chat()
            for us in users_in_chat:
                if chats[chat_numb].get_banned_friend() != 0 and us.get_user_id() \
                        and chats[chat_numb].get_banned_friend_every() == 1:
                    if us.get_friends_count() > 0:
                        us.set_friends_count(us.get_friends_count() - 1)

            if not chats[chat_numb].is_user_in_chat(message.from_user.id):
                chats[chat_numb].add_user_in_chat(message.from_user.id)
            words = chats[chat_numb].get_banned_words()
            text = message.text.lower()
            try:
                for word in words:
                    if re.search(rf'\b{word.lower()}\b', text) and not (message.from_user.id in admins):
                        bot.delete_message(message.chat.id, message.message_id)
                        break
                if not chats[chat_numb].get_links():
                    if re.search(r'\bhttps://\b', message.text):
                        bot.delete_message(message.chat.id, message.message_id)

                if not chats[chat_numb].get_forward() and message.forward_date:
                    bot.delete_message(message.chat.id, message.message_id)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    while True:
        try:
            x = threading.Thread(target=check_banned)
            x.start()
            bot.polling()

        except Exception as e:
            print(e)
            time.sleep(5)
            del bot
            del x
            bot = telebot.TeleBot(token=token)
