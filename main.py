import os
from pydub import AudioSegment
import requests
import telebot
from io import BytesIO

token = '7077413288:AAE-Gy2YWkd0Jp30-bmliHn8DUpTUnn70Ks'
bot = telebot.TeleBot(token)

def save_voice_message(message):
    voice = message.voice
    if voice:
        file_info = bot.get_file(voice.file_id)
        file_url = f"https://api.telegram.org/file/bot{token}/{file_info.file_path}"
        response = requests.get(file_url)
        
        mp3_bytes = BytesIO(response.content)
        audio = AudioSegment.from_file(mp3_bytes, format="ogg")

        out_path = f"voice_messages/{voice.file_id}.wav"
        audio.export(out_path, format="wav")

        bot.reply_to(message, "Голосовое сообщение успешно сохранено и сконвертировано в формат .wav")

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    save_voice_message(message)

if __name__ == '__main__':
  bot.infinity_polling()