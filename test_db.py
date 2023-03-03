import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

table_name = config.get('database', 'table_name')

params = {
    "host": config.get('database', 'host'),
    "port": config.get('database', 'port'),
    "user": config.get('database', 'user'),
    "database": config.get('database', 'name'),
    "password": config.get('database', 'password')
}

# Create the DB
conn = psycopg2.connect(**params)

cur = conn.cursor()

# Execute a SELECT statement to fetch all rows from the posts3 table
cur.execute("SELECT * FROM %s" % table_name)

# Fetch all rows from the result set
rows = cur.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()


