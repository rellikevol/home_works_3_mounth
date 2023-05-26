import sqlite3


def create_db(name: str):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""CREATE TABLE IF NOT EXISTS tasks(
       user_id INT,
       chat_id INT,
       type TEXT,
       interval INT,
       message TEXT,
       time_of_day TEXT,
       tag TEXT);
    """)
    conn.commit()
    cursr.close()
    conn.close()


def insert(name, user_id, chat_id, type, interval, message, time_of_day, tag):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""INSERT INTO tasks(user_id, chat_id, type, interval, message, time_of_day, tag) 
    VALUES(?, ?, ?, ?, ?, ?, ?);""", (user_id, chat_id, type, interval, message, time_of_day, tag))
    conn.commit()
    cursr.close()
    conn.close()


def user_tasks(name, user_id):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM tasks WHERE user_id=?;""", (user_id,)).fetchall()
    conn.commit()
    cursr.close()
    conn.close()
    return res


def delete(name, tag):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""DELETE FROM tasks WHERE tag=?;""", (tag,))
    conn.commit()
    cursr.close()
    conn.close()


def all_tasks(name):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT * FROM tasks;""").fetchall()
    conn.commit()
    cursr.close()
    conn.close()
    return res
