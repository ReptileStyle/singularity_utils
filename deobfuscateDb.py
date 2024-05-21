import sqlite3
from faker import Faker
import random

# Инициализируем Faker для генерации случайных данных
fake = Faker()

def generate_unique_titles(n):
    # Генерируем уникальные названия
    unique_titles = set()
    while len(unique_titles) < n:
        unique_titles.add(fake.word() + ' ' + fake.word())  # Используем fake.word() для случайных слов
    return list(unique_titles)

def replace_titles(connection):
    cursor = connection.cursor()

    # Генерируем уникальные названия для полей title
    tasks_new_titles = generate_unique_titles(10000)  # Генерируем уникальные слова
    projects_new_titles = generate_unique_titles(10000)  # Генерируем уникальные фразы

    # Заменяем title в таблице task
    cursor.execute("SELECT id FROM task")
    task_ids = cursor.fetchall()
    for task_id in task_ids:
        new_title = random.choice(tasks_new_titles)
        cursor.execute("UPDATE task SET title=? WHERE id=?", (new_title, task_id[0]))

    # Заменяем title в таблице project
    cursor.execute("SELECT id FROM project")
    project_ids = cursor.fetchall()
    for project_id in project_ids:
        new_title = random.choice(projects_new_titles)
        cursor.execute("UPDATE project SET title=? WHERE id=?", (new_title, project_id[0]))

    connection.commit()
    cursor.close()

if __name__ == "__main__":
    # Подключаемся к базе данных
    conn = sqlite3.connect('report_backup_2023-09-21_before_files.db')

    # Вызываем функцию для замены title
    replace_titles(conn)

    # Закрываем соединение с базой данных
    conn.close()