from telebot import TeleBot
from dotenv import load_dotenv
import os
load_dotenv("bot_token.env")
TOKEN = os.getenv("TOKEN")

bot = TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler(content_types='text')
def get_text_messages(message):
     bot.send_message(message.from_user.id, message.text)

bot.infinity_polling()