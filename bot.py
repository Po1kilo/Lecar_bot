from telebot import TeleBot
import os

TOKEN = os.getenv("TOKEN")  # Берём TOKEN из настроек Render

bot = TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler(content_types='text')
def get_text_messages(message):
     bot.send_message(message.from_user.id, message.text)

if __name__ == "__main__":
    bot.infinity_polling()
