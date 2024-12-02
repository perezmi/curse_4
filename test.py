import os
import time

def find_latest_file(directory):
    latest_file = None
    latest_time = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_mtime = os.path.getmtime(file_path)

            if file_mtime > latest_time:
                latest_time = file_mtime
                latest_file = file_path

    return latest_file

# Укажите директорию, которую хотите проверить
directory = '/home/verz/Документы/Obsidian Vault'  # Замените на нужный путь
latest_file = find_latest_file(directory)

if latest_file:
    print(f"Последний изменённый файл: {latest_file}")
else:
    print("В указанной директории нет файлов.")
