from telebot import types
import telebot
import time
import re

bot = telebot.TeleBot(token="1427693199:AAGnuGWcgwUy5tLlE7_GKyomLCHKY_T5mZI")

users = []
chats = []
bot_id = 1427693199


class User:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__can_change = False
        self.__can_change_words = False
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

    def get_number_chat(self):
        return self.__number_chat

    def set_number_chat(self, number_chat):
        self.__number_chat = number_chat


class Chat:
    def __init__(self, owner_id, chat_id):
        self.__owner_id = owner_id
        self.__chat_id = chat_id
        self.__banned_words = []
        self.__links = True

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


def chat_number(user_id):
    chat_numb = 0
    for us in users:
        if us.get_user_id() == user_id:
            chat_numb = us.get_number_chat()
    return chat_numb


def start_buttons():
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Новости", callback_data="news")
    but_2 = types.InlineKeyboardButton(text="Поддержка", url="https://t.me/N0tdefined")
    but_3 = types.InlineKeyboardButton(text="Настройка чатов", callback_data="my_chats")
    but_4 = types.InlineKeyboardButton(text="Как пользоваться", callback_data="info")
    key.add(but_1, but_2)
    key.add(but_3, but_4)
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
            users.append(User(message.chat.id))
        else:
            text = "Выберите действие"

        bot.send_message(message.chat.id, text, reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "start")
def start(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
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
        except Exception:
            pass
        number = get_user(call.from_user.id)
        users[number].set_can_change(True)
        txt = "Введите номер чата\n"
        for i in range(len(names)):
            txt += names[i] + " - " + str(i + 1) + "\n"
        bot.send_message(call.from_user.id, txt)


@bot.message_handler(commands=[""])
def chat_settings(message):
    chat_numb = chat_number(message.chat.id)

    if chats[chat_numb - 1].get_links():
        link_txt = "(разрешены)"
    else:
        link_txt = "(запрещены)"
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Запрещённые слова", callback_data="banned_words")
    but_2 = types.InlineKeyboardButton(text="Ссылки" + link_txt, callback_data="url_forward")
    but_3 = types.InlineKeyboardButton(text="Назад", callback_data="start")
    key.add(but_1, but_2)
    key.add(but_3)
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "chat_settings")
def chat_settings(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    chat_numb = chat_number(call.from_user.id)

    if chats[chat_numb - 1].get_links():
        link_txt = "(разрешены)"
    else:
        link_txt = "(запрещены)"
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Запрещённые слова", callback_data="banned_words")
    but_2 = types.InlineKeyboardButton(text="Ссылки" + link_txt, callback_data="url_forward")
    but_3 = types.InlineKeyboardButton(text="Назад", callback_data="start")
    key.add(but_1, but_2)
    key.add(but_3)
    bot.send_message(call.from_user.id, "Выберите действие", reply_markup=key, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == "banned_words")
def banned_words(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    chat_numb = chat_number(call.from_user.id)
    banned_w = chats[chat_numb - 1].get_banned_words()
    if banned_w:
        bot.send_message(call.from_user.id, "Запрещённые слова - " + banned_w)
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
    bot.delete_message(call.message.chat.id, call.message.message_id)
    number = get_user(call.from_user.id)
    users[number].set_can_change_words(True)
    bot.send_message(call.from_user.id, "Введите запрещённые слова через пробел\nПример: один два три")


@bot.callback_query_handler(func=lambda call: call.data == "url_forward")
def url_forward(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    chat_numb = chat_number(call.from_user.id)
    chats[chat_numb - 1].change_links()
    chat_settings(call)


@bot.message_handler()
def message_handler(message):
    print(message)
    print(message.text)
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
                chats[chat_numb - 1].set_banned_words(words)
                us.set_can_change_words(False)
                chat_settings(message)

        if not is_any:
            bot.send_message(message.chat.id, "Извините, я не понял.")
    else:
        for admin in bot.get_chat_administrators(message.chat.id):
            if admin.status == "creator" and not is_creator(admin.user.id):
                chats.append(Chat(admin.user.id, message.chat.id))
        chat_numb = chat_number(message.chat.id)
        words = chats[chat_numb - 1].get_banned_words()
        message.text.lower()

        for word in words:
            print(word)
            print(message.text)
            if re.search(rf'\b{word}\b', message.text):
                bot.delete_message(message.chat.id, message.message_id)
                break
        if not chats[chat_numb - 1].get_links():
            if re.search(r'\bhttps://\b', message.text):
                bot.delete_message(message.chat.id, message.message_id)


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(e)
            time.sleep(15)

