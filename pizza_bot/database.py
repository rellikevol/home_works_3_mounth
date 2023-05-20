import sqlite3

def create_db(name: str):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""CREATE TABLE IF NOT EXISTS users(
       first_name TEXT,
       last_name TEXT,
       username TEXT,
       user_id INT,
       phone_number TEXT);
    """)
    conn.commit()
    cursr.execute("""CREATE TABLE IF NOT EXISTS adress(
           user_id INT,
           adress_longitude REAL,
           adress_latitude REAL);
        """)
    conn.commit()
    cursr.execute("""CREATE TABLE IF NOT EXISTS orders(
               user_id INT,
               title TEXT,
               address_destination TEXT,
               datetime_order TEXT);
            """)
    conn.commit()
    cursr.close()
    conn.close()

def is_user_exist(name: str, user_id: int) -> bool:
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("SELECT * FROM users WHERE user_id=?;", (user_id, )).fetchall()
    cursr.close()
    conn.close()
    if len(res) == 0:
        return False
    else:
        return True
def is_location_exist(name: str, user_id: int) -> bool:
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("SELECT * FROM adress WHERE user_id=?;", (user_id, )).fetchall()
    cursr.close()
    conn.close()
    if len(res) == 0:
        return False
    else:
        return True

def append_user(name: str, firstname, lastname, username, userid):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""INSERT INTO users(first_name, last_name, username, user_id) VALUES (?, ?, ?, ?);""",
                  (firstname, lastname, username, userid))
    conn.commit()
    cursr.close()
    conn.close()

def append_number(name, number, userid):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    cursr.execute("""UPDATE users SET phone_number = ? WHERE user_id = ?;""",
                  (number, userid))
    conn.commit()
    cursr.close()
    conn.close()

def append_location(name, userid, longitude, latitude):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    if is_location_exist(name, userid):
        cursr.execute("""UPDATE adress SET adress_longitude = ?, adress_latitude = ? WHERE user_id = ?;""",
                      (longitude, latitude, userid))
    else:
        cursr.execute("""INSERT INTO adress(user_id, adress_longitude, adress_latitude) VALUES (?, ?, ?);""",
                      (userid, longitude, latitude))
    conn.commit()
    cursr.close()
    conn.close()

def check_location_exist(name: str, userid):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    res = cursr.execute("""SELECT adress_longitude, adress_latitude FROM adress WHERE user_id = ?;""",
                        (userid,)).fetchall()
    cursr.close()
    conn.close()
    if len(res) > 0:
        return True
    else:
        return False

def set_title(name: str, user_id: int, title: str, datetime_order):
    conn = sqlite3.connect(name)
    cursr = conn.cursor()
    adress = cursr.execute("""SELECT adress_longitude, adress_latitude FROM adress WHERE user_id = ?;""",
                           (user_id,)).fetchall()
    res = 'adress_longitude: ' + str(adress[0][0]) + " adress_latitude: " + str(adress[0][1])
    cursr.execute("""INSERT INTO orders(user_id, title, address_destination, datetime_order)
                    VALUES (?, ?, ?, ?);""", (user_id, title, res, datetime_order))
    conn.commit()
    cursr.close()
    conn.close()
