import os
import sys

import google.generativeai as genai
import telebot
from dotenv import load_dotenv

load_dotenv(sys.argv[1])

AI_GOOGLE_API = os.getenv("AI_GOOGLE_API")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


def google_ai(question):
    if not AI_GOOGLE_API:
        return "silakan periksa AI_GOOGLE_API anda di file env"
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
        bot.reply_to(message, "👋 Hai, Perkenalkan saya ai google telegram bot. Dan saya adalah robot kecerdasan buatan dari ai.google.dev, dan saya siap menjawab pertanyaan yang Anda berikan")
    else:
        msg = bot.reply_to(message, result)
        try:
            result = google_ai(message.text)
        except Exception as error:
            result = str(error)
        bot.edit_message_text(result, message.chat.id, msg.message_id)


bot.infinity_polling()
