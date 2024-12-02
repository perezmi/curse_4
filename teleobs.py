import os
import telebot
import time
from datetime import datetime
TOKEN="5507680935:AAHu8UgGzCOFQgd-vXVsBLF5PUfMvd7AGps"



import os
import time

def find_latest_file(directory):
    latest_file = None
    latest_time = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_mtime = os.path.getmtime(file_path)

            if file_mtime > latest_time and file.endswith('.md'):
                latest_time = file_mtime
                latest_file = file_path

    return latest_file
def append_to_file(file_path, text_to_append):
    try:
        with open(file_path, 'a') as file:  # Открываем файл в режиме добавления
            file.write(text_to_append + '\n')  # Добавляем текст с новой строки
        print(f"Строка была успешно добавлена в файл: {file_path}")
    except FileNotFoundError:
        print(f"Файл по указанному пути '{file_path}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при работе с файлом: {e}")
# Укажите директорию, которую хотите проверить

directory = 'Универ'  # Замените на нужный путь
latest_file = find_latest_file(directory)
now=datetime.now()
photo_dir=os.path.dirname(latest_file)+"/фото/"+now.strftime("%d.%m.%y")+"/"

if not os.path.exists(photo_dir):
    os.makedirs(photo_dir)
print(latest_file,"\n",photo_dir)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Получаем фотографию с наибольшим разрешением
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    
    # Скачиваем файл
    downloaded_file = bot.download_file(file_info.file_path)
    now=datetime.now()
    str_now=now.strftime("%H:%M")
    # Создаем путь для сохранения
    file_path = os.path.join(photo_dir, "фото "+str_now+".jpg")
    
    # Записываем файл на диск
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    append_to_file(latest_file,"![["+photo_dir+"фото "+str_now+".jpg"+"]]")
    bot.reply_to(message, "Пиздец")

bot.polling()
