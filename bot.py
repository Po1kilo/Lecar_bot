import os
from flask import Flask, abort, request
from telebot import TeleBot, types

# Telegram bot token from environment (Render env var)
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN env var is required")

# Webhook configuration: prefer Render external URL, fallback to explicit WEBHOOK_URL
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_BASE = os.getenv("WEBHOOK_URL") or os.getenv("RENDER_EXTERNAL_URL")
if not WEBHOOK_BASE:
    raise RuntimeError("WEBHOOK_URL or RENDER_EXTERNAL_URL env var is required")
WEBHOOK_URL = f"{WEBHOOK_BASE}{WEBHOOK_PATH}"

bot = TeleBot(TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.send_chat_action(message.chat.id, "typing")  # имитация набора
    text = (
        "Привет! 👋\n\n"
        "Я бот для проверки статуса заказа.\n"
        "Просто отправь мне *номер заказа*, а я верну его текущий статус.\n\n"
        "Сейчас я работаю в тестовом режиме — как только коллеги доделают эндпоинт, "
        "здесь появится живой статус из системы."
        )

    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("📦 Ввести номер заказа", callback_data="enter_order"),
        InlineKeyboardButton("🌐 Перейти на сайт Lecar.ru", url="https://lecar.ru"),
    )

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")



@bot.message_handler(content_types=["text"])
def echo_text(message):
    bot.send_chat_action(message.chat.id, "typing")  # имитация набора
    bot.send_message(message.chat.id, message.text)


@app.route("/", methods=["GET"])
def health():
    return "OK", 200


@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if request.headers.get("content-type") != "application/json":
        abort(403)
    json_str = request.get_data(as_text=True)
    update = types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200


def setup_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)


if __name__ == "__main__":
    setup_webhook()
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
