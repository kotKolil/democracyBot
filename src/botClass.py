import telebot
from telebot import types
import json

class botClass(object):

    def __init__(self, bot_token:str):
        self.bot = telebot.TeleBot(bot_token)
        self.data = dict()

        self.bot.message_handler(commands=['start'])(self.start_command)
        self.bot.message_handler(commands=['help'])(self.help_command)
        self.bot.message_handler(commands=['promote_to_admin'])(self.promote_to_admin)

        self.bot.callback_query_handler(func=lambda call: True)(self.callback_command)

    def start_command(self, message):
        if message.chat.type == "supergroup":
            self.bot.send_message(message.chat.id, "I ready to bring a democracy!")
        elif message.chat.type == "private":
            self.bot.send_message(message.from_user.id, "hello, comrade! Add me to chat that I could bring a democracy!")

    def help_command(self, message):
        self.bot.send_message(message.chat.id, "This bot was created to add new chat administrators by anonymous voting. If the candidate gets more than half of the votes, he will become the new administrator! Also, he can be removed from his duty via same method. To promote to admin, send command /promote_to_admin and nick of user that you want to become a new admin")

    def promote_to_admin(self, message):
        if message.chat.type == "supergroup":
            if len(message.text.split(" ")) == 1:
                self.bot.send_message(message.chat.id, "please, provide me a username")
            elif len(message.text.split(" ")) == 2:
                username = message.text.split(" ")[1]
                markup = types.InlineKeyboardMarkup()

                self.data[username] = dict()
                self.data[username]["yes"] = []
                self.data[username]["no"] = []

                yes_button = types.InlineKeyboardButton("yes", callback_data =
                    json.dumps({"action": "yes", "candidate": username})
                )
                markup.add(yes_button)

                no_button = types.InlineKeyboardButton("no", callback_data =
                    json.dumps({"action": "no", "candidate": username})
                )
                markup.add(no_button)

                self.bot.send_message(
                    message.chat.id,
                    f"promote {username} to admin?",
                    reply_markup=markup
                )


        elif message.chat.type == "private":
            self.bot.send_message(message.chat.id, "add me to group that i could bring a democracy!")


    def callback_command(self, call):
        data = json.loads(call.data)
        username = call.from_user.username
        candidate = data["candidate"]

        action = data["action"]

        if action == "yes":
            if username in self.data[candidate]["no"]:
                self.data[candidate]["no"].remove(username)
            if username in self.data[candidate]["yes"]:
                self.data[candidate]["yes"].remove(username)
            else:
                self.data[candidate]["yes"].append(username)

        elif action == "no":
            if username in self.data[candidate]["yes"]:
                self.data[candidate]["yes"].remove(username)
            if username in self.data[candidate]["no"]:
                self.data[candidate]["no"].remove(username)
            else:
                self.data[candidate]["no"].append(username)

        print(self.data)
        self.bot.answer_callback_query(call.id, "you voted")

    def start(self):
        self.bot.polling(none_stop=True, interval=0)


