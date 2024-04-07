import telebot
import pydub
import os

token = '7077413288:AAE-Gy2YWkd0Jp30-bmliHn8DUpTUnn70Ks'
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['voice'])
def save_voice_message(message):
    voice = message.voice
    if voice:
        file_info = bot.get_file(voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = f"voice_messages/{voice.file_id}.ogg"  # Путь для сохранения файла
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Голосовое сообщение успешно сохранено")

def conver_audio_messages_to_wav(): 
    pass


if __name__ == '__main__':
  bot.infinity_polling()