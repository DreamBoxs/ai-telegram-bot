import os
import sys
from io import BytesIO

import google.generativeai as genai
import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv(sys.argv[1])

AI_GOOGLE_API = os.getenv("AI_GOOGLE_API")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = telebot.TeleBot(BOT_TOKEN)

text = """
user_id: {}
name: {} {}

msg: {}
"""


def get_text(message):
    reply_text = message.reply_to_message.text or message.reply_to_message.caption if message.reply_to_message else ""
    user_text = message.text.split(None, 1)[1] if len(message.text.split()) >= 2 else ""
    return f"{user_text}\n\n{reply_text}" if reply_text and user_text else reply_text + user_text


def google_ai(question):
    if not AI_GOOGLE_API:
        return "Silakan periksa AI_GOOGLE_API Anda di file env"
    genai.configure(api_key=AI_GOOGLE_API)
    model = genai.GenerativeModel(model_name="gemini-1.0-pro")
    convo = model.start_chat(history=[])
    convo.send_message(question)
    return convo.last.text


def send_large_output(message, output, msg):
    if len(output) <= 4000:
        bot.send_message(message.chat.id, output, parse_mode='Markdown')
    else:
        with BytesIO(str.encode(str(output))) as out_file:
            out_file.name = "result.txt"
            bot.send_document(message.chat.id, out_file)
    bot.delete_message(message.chat.id, msg.message_id)


def owner_notif(func):
    def function(message):
        if message.from_user.id != OWNER_ID:
            bot.send_message(OWNER_ID, text.format(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.text))
        return func(message)
    return function


@bot.message_handler(func=lambda message: True)
@owner_notif
def google(message):
    if message.text.startswith("/start"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Repository", url="https://github.com/DreamBoxs/ai-telegram-bot"), types.InlineKeyboardButton("Credit", url="https://t.me/NorSodikin"))
        bot.reply_to(message, "👋 Hai, Perkenalkan saya ai google telegram bot. Dan saya adalah robot kecerdasan buatan dari ai.google.dev, dan saya siap menjawab pertanyaan yang Anda berikan", reply_markup=markup)
    else:
        msg = bot.reply_to(message, "Silahkan tunggu...")
        try:
            result = google_ai(get_text(message))
            send_large_output(message, result, msg)
        except Exception as error:
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=str(error), parse_mode='Markdown')


bot.infinity_polling()
