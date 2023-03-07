import os
import psycopg2.errors
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

table_name = config.get('database', 'table_name')
db = config.get('database', 'name')
directory = "content"

params = {
    "host": config.get('database', 'host'),
    "port": config.get('database', 'port'),
    "user": config.get('database', 'user'),
    "password": config.get('database', 'password')
}

# Create the DB
conn = psycopg2.connect(**params)
conn.autocommit = True
cursor = conn.cursor()
try:
    cursor.execute("DROP DATABASE %s" % db)
except Exception as e:
    print(e)

try:
    cursor.execute("CREATE DATABASE %s" % db)
except psycopg2.errors.lookup("42P04") as e:  # duplicate db, this is very unclear I know
    print(e)
cursor.close()
conn.close()

print("Created database...")

# Add table and contents to the DB
conn = psycopg2.connect(**params, database=db)
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS %s (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255),
    content TEXT
);

''' % table_name
cursor.execute(create_table_query)
conn.commit()

#
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        with open(f) as f1:
            title = f1.readline().strip()
            content = "\n".join([line.strip() for line in f1])
            cursor.execute("INSERT INTO %s (title, content) VALUES ('CLOUD! %s', '%s')" % (table_name, title, content))

conn.commit()

cursor.close()
conn.close()

print("Data loaded into database...")
print("Done")
