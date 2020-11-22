from telebot import types
import telebot
import time
import re
import threading

bot = telebot.TeleBot(token="1427693199:AAGnuGWcgwUy5tLlE7_GKyomLCHKY_T5mZI")

users = []
chats = []


class UserInBot:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__can_change = False
        self.__can_change_words = False
        self.__can_change_time_banned = False
        self.__can_change_group_banned = False
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


class Chat:
    def __init__(self, owner_id, chat_id):
        self.__owner_id = owner_id
        self.__chat_id = chat_id
        self.__banned_words = []
        self.__links = True
        self.__forward = True
        self.__banned_time = 0
        self.__banned_chanel = 0
        self.__users_in_chat = []

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

    def get_banned_time(self):
        return self.__banned_time

    def set_banned_time(self, banned_time):
        self.__banned_time = banned_time

    def get_banned_chanel(self):
        return self.__banned_chanel

    def set_banned_chanel(self, banned_chanel):
        self.__banned_chanel = banned_chanel


def is_user(user_id):
    for us in users:
        if user_id == us.get_user_id():
            return True
    return False


def is_creator(user_id):
    for chat in chats:
        if user_id == chat.get_owner_id():
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

    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Запрещённые слова", callback_data="banned_words")
    but_2 = types.InlineKeyboardButton(text="Ссылки" + link_txt, callback_data="url")
    but_3 = types.InlineKeyboardButton(text="Пересланные сообщения" + forward_txt, callback_data="forwarded")
    but_4 = types.InlineKeyboardButton(text="Запрет писать", callback_data="banned_user")
    but_5 = types.InlineKeyboardButton(text="Назад", callback_data="start")
    key.add(but_1, but_2)
    key.add(but_3)
    key.add(but_4)
    key.add(but_5)
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
        except Exception:
            print(e)
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
    bot.send_message(call.from_user.id, "Добавьте бота в свой чат, повысьте его права"
                                        " до администратора, далее создатель чата может"
                                        " настроить бота (Мои чаты -> Настройки)")
    start(call)


@bot.callback_query_handler(func=lambda call: call.data == "my_chats")
def my_chats(call):
    names = []
    for chat in chats:
        if chat.get_owner_id() == call.from_user.id:
            names.append(bot.get_chat(chat.get_chat_id()).title)

    if not is_creator(call.from_user.id):
        bot.send_message(call.from_user.id, "У вас нет чатов с ботом")
    else:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            print(e)
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
        print(e)
    chat_numb = chat_number(call.from_user.id)
    key = settings_buttons(chat_numb)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "banned_words")
def banned_words(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)
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
        print(e)
    number = get_user(call.from_user.id)
    users[number].set_can_change_words(True)
    bot.send_message(call.from_user.id, "Введите запрещённые слова через пробел\nПример: один два три")


@bot.callback_query_handler(func=lambda call: call.data == "url")
def url(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].change_links()
    chat_settings(call)


@bot.callback_query_handler(func=lambda call: call.data == "forwarded")
def forwarded(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb].change_forward()
    chat_settings(call)


@bot.callback_query_handler(func=lambda call: call.data == "banned_user")
def banned_user(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)
    key = types.InlineKeyboardMarkup()
    chat_numb = chat_number(call.from_user.id)
    if chats[chat_numb].get_banned_time() == 0:
        banned_time_txt = "(нет)"
    else:
        banned_time_txt = f"({chats[chat_numb].get_banned_time()} минут)"

    if chats[chat_numb].get_banned_chanel() == 0:
        banned_chanel_txt = "(нет)"
    else:
        banned_chanel_txt = f"({chats[chat_numb].get_banned_chanel()})"
    but_1 = types.InlineKeyboardButton(text="Запрет писать первое время " + banned_time_txt, callback_data="banned_by_time")
    but_2 = types.InlineKeyboardButton(text="Запрет писать если не в канале" + banned_chanel_txt, callback_data="banned_by_chanel")
    but_3 = types.InlineKeyboardButton(text="Назад", callback_data="chat_settings")
    key.add(but_1)
    key.add(but_2)
    key.add(but_3)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "banned_by_time")
def banned_by_time(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)
    number = get_user(call.from_user.id)
    users[number].set_can_change_time_banned(True)
    bot.send_message(call.from_user.id, "Введите время (в минутах) сколько нельзя писать новым участники группы")


@bot.callback_query_handler(func=lambda call: call.data == "banned_by_chanel")
def banned_by_chanel(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)

    number = get_user(call.from_user.id)
    users[number].set_can_change_group_banned(True)
    bot.send_message(call.from_user.id, "Добавьте бота в канал и после этого парешлите "
                                        "боту любой пост с канала где есть текст.")


@bot.message_handler(content_types=["new_chat_members"])
def new_member(message):
    chat_numb = get_chat(message.chat.id)
    if not chats[chat_numb].is_user_in_chat(message.from_user.id):
        chats[chat_numb].add_user_in_chat(message.from_user.id)

    users_in_chat = chats[chat_numb].get_users_in_chat()
    for us in users_in_chat:
        if us.get_user_id() == message.from_user.id:
            if chats[chat_numb].get_banned_time() > 0:
                us.set_time_of_ban(chats[chat_numb].get_banned_time())
                us.set_when_banned(time.time())
                us.set_is_time_banned(True)
                bot.restrict_chat_member(chats[chat_numb].get_chat_id(), us.get_user_id())

            if chats[chat_numb].get_banned_chanel() != 0:
                try:
                    if bot.get_chat_member(chats[chat_numb].get_chat_banned(), message.from_user.id):
                        pass
                except Exception as e:
                    bot.restrict_chat_member(chats[chat_numb].get_chat_id(), us.get_user_id())
                    us.set_is_group_banned(True)

    text = f"Добро пожаловать, {message.from_user.first_name}"
    bot.send_message(message.chat.id, text)
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=["left_chat_member"])
def left_member(message):
    bot.delete_message(message.chat.id, message.message_id)


def check_banned():
    old_time = time.time()
    while True:
        if time.time() - old_time > 5:
            for chat in chats:
                users_in_chat = chat.get_users_in_chat()
                for us in users_in_chat:
                    try:
                        if time.time() - us.get_when_banned() > us.get_time_of_ban() * 60 and us.get_is_time_banned():
                            bot.promote_chat_member(chat.get_chat_id(), us.get_user_id())
                            us.set_is_time_banned(False)
                    except Exception as e:
                        print(e)
                    try:
                        if us.get_is_group_banned() and bot.get_chat_member(chat.get_banned_chanel(), us.get_user_id()):
                            us.set_is_group_banned(False)
                            bot.promote_chat_member(chat.get_chat_id(), us.get_user_id())
                    except Exception as e:
                        print(e)

            old_time = time.time()


@bot.message_handler()
def message_handler(message):
    if message.chat.id > 0:
        names = []
        for chat in chats:
            if chat.get_owner_id() == message.chat.id:
                names.append(bot.get_chat(chat.get_chat_id()).title)

        is_any = False
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
                chat_numb = chat_number(message.chat.id)
                words = message.text
                words = words.split(" ")
                chats[chat_numb].set_banned_words(words)
                us.set_can_change_words(False)
                chat_settings(message)
            elif us.get_user_id() == message.chat.id and us.get_can_change_time_banned():
                is_any = True
                if message.text.isdigit():
                    if 0 < int(message.text) <= 10080:
                        chat_numb = chat_number(message.chat.id)
                        chats[chat_numb].set_banned_time(int(message.text))
                        us.set_can_change_time_banned(False)
                        chat_settings(message)
                    else:
                        bot.send_message(message.chat.id, "Число должно быть в диапазоне 0-10080")
                else:
                    bot.send_message(message.chat.id, "Некорректный ввод.")

            elif us.get_user_id() == message.chat.id and us.get_can_change_group_banned():
                if message.forward_from_chat:
                    chat_numb = chat_number(message.chat.id)
                    chats[chat_numb].set_banned_chanel(message.forward_from_chat.id)
                    print(message.forward_from_chat.title)
                    is_any = True
                    chat_settings(message)

        if not is_any:
            bot.send_message(message.chat.id, "Извините, я не понял.")
    else:
        for chat in chats:
            if message.chat.id == chat.get_chat_id() and not chat.is_user_in_chat(message.chat.id):
                chat.add_users_in_chat(message.chat.id)

        for admin in bot.get_chat_administrators(message.chat.id):
            if admin.status == "creator" and not is_creator(admin.user.id):
                chats.append(Chat(admin.user.id, message.chat.id))
        chat_numb = get_chat(message.chat.id)
        if not chats[chat_numb].is_user_in_chat(message.from_user.id):
            chats[chat_numb].add_user_in_chat(message.from_user.id)
        words = chats[chat_numb].get_banned_words()
        message.text.lower()
        try:
            for word in words:
                if re.search(rf'\b{word}\b', message.text):
                    bot.delete_message(message.chat.id, message.message_id)
                    break
            if not chats[chat_numb].get_links():
                if re.search(r'\bhttps://\b', message.text):
                    bot.delete_message(message.chat.id, message.message_id)

            if not chats[chat_numb].get_forward() and message.forward_date:
                bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            print(e)
        # bot.get_chat_member(-1001302195525, 1070942344)
        # bot.get_chat_member(-1001302195525, 443109443)
        #
        # print("12", bot.get_chat_member(-1001431663155, 443109443))


if __name__ == "__main__":
    while True:
        try:
            x = threading.Thread(target=check_banned)
            x.start()
            bot.polling(none_stop=True, interval=0)

        except Exception as e:
            print(e)
            time.sleep(10)

