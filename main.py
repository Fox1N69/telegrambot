from pydub import AudioSegment
import requests
import telebot
import cv2
import numpy as np
from io import BytesIO

token = '7077413288:AAE-Gy2YWkd0Jp30-bmliHn8DUpTUnn70Ks'
bot = telebot.TeleBot(token)

audio_messages={}
def save_voice_message(message):
    user_id = message.from_user.id
    file_id = message.voice.file_id

    if user_id not in audio_messages:
        audio_messages[user_id] = []

    file = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{token}/{file.file_path}"
    response = requests.get(file_url)

    audio = AudioSegment.from_file(BytesIO(response.content), format="ogg")
    path = f"voice_messages/{user_id}_{len(audio_messages[user_id])}.wav"
    audio.export(path, format="wav", parameters=["-ar", "16000"])

    audio_messages[user_id].append(path)

    bot.reply_to(message, "Голосовое сообщение было конверированно в wav и сохранено в папку voice_messages")


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    save_voice_message(message)

def detect_faces_in_photo(image_bytes):
    image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces) > 0


@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{token}/{file.file_path}"
    response = requests.get(file_url)
    if detect_faces_in_photo(response.content):
        file_path = f"photo_with_faces/photo_{file_id}.jpg"
        with open(file_path, 'wb') as image_file:
            image_file.write(response.content)
        bot.send_message(message.chat.id, "Фото было сохранено в папку photo_with_face")
    else:
        bot.send_message(message.chat.id, "На фото не обнаруженны лица")



if __name__ == '__main__':
  bot.infinity_polling()