import sqlite3

#work with database
def messages():
    conn = sqlite3.connect('artikles.db')
    cursr = conn.cursor()
    cursr.execute('SELECT * FROM messages')
    res = cursr.fetchall()
    cursr.close()
    conn.close()
    return res


def articles():
    conn = sqlite3.connect('artikles.db')
    cursr = conn.cursor()
    cursr.execute('SELECT * FROM articles')
    res = cursr.fetchall()
    cursr.close()
    conn.close()
    return res
