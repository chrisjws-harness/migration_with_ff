import sqlite3
import os

directory = 'content'

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        with open(f) as f1:
            title = f1.readline().strip()
            content = "\n".join([line.strip() for line in f1])
            cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))


connection.commit()
connection.close()
