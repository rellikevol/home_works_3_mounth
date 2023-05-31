from dotenv import load_dotenv
import psycopg2, os

load_dotenv('.env')

connect = psycopg2.connect(
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_USER_PASSWORD'),
    database=os.environ.get('DB_NAME'),
    host=os.environ.get('DB_HOST')
)
connect.autocommit=True

cursor = connect.cursor()
cursor.execute('SELECT VERSION();')
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(100),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    age INTEGER
);""")
cursor.execute("""INSERT INTO users VALUES (%s, %s, %s, %s);""", ('hello', 'ilja', 'gaida', 33))

