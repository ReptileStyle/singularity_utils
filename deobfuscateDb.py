import sqlite3

from delta import Delta
from faker import Faker
import random
# from quill_delta import Delta

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

def replace_task_notes_with_question_marks(connection):
    cursor = connection.cursor()

    # Replace all values in the note column of the task table with '????????'
    cursor.execute("UPDATE task SET note='????????'")

    connection.commit()
    cursor.close()

def generate_unique_content(n):
    # Generate unique delta content
    unique_contents = set()
    while len(unique_contents) < n:
        words = ' '.join(fake.words(random.randint(5, 15)))  # Random words between 5 and 15
        delta_content = f'[{{"insert":"{words}\\n"}}]'
        unique_contents.add((delta_content, words))


    return list(unique_contents)

def replace_content(connection):
    cursor = connection.cursor()

    # Generate unique delta content for fields content
    new_contents = generate_unique_content(10000)  # Generate unique content

    # Replace content in notes table
    cursor.execute("SELECT id FROM note")
    note_ids = cursor.fetchall()
    for note_id in note_ids:
        new_content, plain_text = random.choice(new_contents)
        cursor.execute("UPDATE note SET content=?, plainText=? WHERE id=?", (str(new_content), plain_text, note_id[0]))

    connection.commit()
    cursor.close()

if __name__ == "__main__":
    # Подключаемся к базе данных
    conn = sqlite3.connect('sqlite.db')

    # replace_task_notes_with_question_marks(conn)
    # Вызываем функцию для замены title
    # replace_titles(conn)
    # replace_(conn)

    replace_content(conn)

    # Закрываем соединение с базой данных
    conn.close()