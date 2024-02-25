import os
import sys

import google.generativeai as genai
import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv(sys.argv[1])

AI_GOOGLE_API = os.getenv("AI_GOOGLE_API")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


def get_text(message):
    reply_text = message.reply_to_message.text or message.reply_to_message.caption if message.reply_to_message else ""
    user_text = message.text.split(None, 1)[1] if len(message.text.split()) >= 2 else ""
    return f"{user_text}\n\n{reply_text}" if reply_text and user_text else reply_text + user_text


def google_ai(question):
    if not AI_GOOGLE_API:
        return "Silakan periksa AI_GOOGLE_API Anda di file env"
    genai.configure(api_key=AI_GOOGLE_API)
    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)
    convo = model.start_chat(history=[])
    convo.send_message(question)
    return convo.last.text


@bot.message_handler(func=lambda message: True)
def google(message):
    if message.text.startswith("/start"):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Repository", url="https://github.com/DreamBoxs/ai-telegram-bot"))
        markup.add(types.InlineKeyboardButton("Credit", url="https://t.me/NorSodikin"))
        bot.reply_to(message, "👋 Hai, Perkenalkan saya ai google telegram bot. Dan saya adalah robot kecerdasan buatan dari ai.google.dev, dan saya siap menjawab pertanyaan yang Anda berikan", reply_markup=markup)
    else:
        msg = bot.reply_to(message, "Silahkan tunggu...")
        try:
            result = google_ai(get_text(message))
        except Exception as error:
            result = str(error)
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=result, parse_mode='Markdown')


bot.infinity_polling()
