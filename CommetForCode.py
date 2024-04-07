from pydub import AudioSegment
import requests
import telebot
import cv2
import numpy as np
from io import BytesIO

token = '7077413288:AAE-Gy2YWkd0Jp30-bmliHn8DUpTUnn70Ks'
bot = telebot.TeleBot(token)

audio_messages = {}  # Инициализация словаря для хранения аудио-сообщений

# Функция для сохранения голосовых сообщений
def save_voice_message(message):
    user_id = message.from_user.id  # Получение ID пользователя
    file_id = message.voice.file_id  # Получение ID аудиофайла сообщения

    if user_id not in audio_messages:  # Проверка наличия записей для пользователя
        audio_messages[user_id] = []  # Создание записей, если их нет

    file = bot.get_file(file_id)  # Получение информации о файле аудиосообщения
    file_url = f"https://api.telegram.org/file/bot{token}/{file.file_path}"  # URL для загрузки файла
    response = requests.get(file_url)  # Получение содержимого файла по URL

    audio = AudioSegment.from_file(BytesIO(response.content), format="ogg")  # Создание объекта AudioSegment из файла
    path = f"voice_messages/{user_id}_{len(audio_messages[user_id])}.wav"  # Путь для сохранения аудиофайла
    audio.export(path, format="wav", parameters=["-ar", "16000"])  # Экспорт аудиофайла в формат WAV

    audio_messages[user_id].append(path)  # Добавление пути к аудиофайлу в записи пользователя

    bot.reply_to(message, "Голосовое сообщение сконвертировано в WAV и сохранено в папку voice_messages")  # Отправка сообщения пользователю

# Обработчик для голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    save_voice_message(message)  # Вызов функции сохранения голосового сообщения

# Функция для обнаружения лиц на фотографии
def detect_faces_in_photo(image_bytes):
    image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)  # Декодирование изображения
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # Инициализация каскада Хаара
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))  # Обнаружение лиц на изображении
    return len(faces) > 0  # Возврат результата: True, если лица обнаружены, иначе False

# Обработчик для фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo_message(message):
    file_id = message.photo[-1].file_id  # Получение ID фотографии
    file = bot.get_file(file_id)  # Получение информации о файле
    file_url = f"https://api.telegram.org/file/bot{token}/{file.file_path}"  # URL для загрузки файла
    response = requests.get(file_url)  # Получение содержимого файла

    if detect_faces_in_photo(response.content):  # Проверка наличия лиц на фотографии
        file_path = f"photo_with_faces/photo_{file_id}.jpg"  # Путь для сохранения фотографии с лицами
        with open(file_path, 'wb') as image_file:  # Открытие файла для записи
            image_file.write(response.content)  # Запись содержимого файла
        bot.send_message(message.chat.id, "Фото сохранено в папку photo_with_face")  # Отправка сообщения о сохранении
    else:
        bot.send_message(message.chat.id, "На фото не обнаружены лица")  # Отправка сообщения о отсутствии лиц на фото

if __name__ == '__main__':
    bot.infinity_polling()  # Начало бесконечного опроса бота