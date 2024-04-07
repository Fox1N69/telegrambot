import telebot
import os
from pydub import AudioSegment

token = '7077413288:AAE-Gy2YWkd0Jp30-bmliHn8DUpTUnn70Ks'
bot = telebot.TeleBot(token)

def convert_to_wav(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="ogg")
    audio = audio.set_frame_rate(16000).set_channels(1)  # Устанавливаем частоту дискретизации 16 кГц и 1 канал
    audio.export(output_path, format="wav")

@bot.message_handler(content_types=['voice'])
def save_voice_message(message):
    voice = message.voice
    if voice:
        file_info = bot.get_file(voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        ogg_file_path = f"voice_messages/{voice.file_id}.ogg"  # Путь для сохранения файла в формате .ogg
        wav_file_path = f"voice_messages/{voice.file_id}.wav"  # Путь для сохранения конвертированного файла в формате .wav

        # Сохраняем аудио сообщение в формате .ogg
        with open(ogg_file_path, 'wb') as ogg_file:
            ogg_file.write(downloaded_file)
        
        # Конвертируем аудиосообщение в формат .wav с частотой дискретизации 16 кГц
        convert_to_wav(ogg_file_path, wav_file_path)

        bot.reply_to(message, "Голосовое сообщение успешно сохранено и сконвертировано в формат .wav")


if __name__ == '__main__':
  bot.infinity_polling()