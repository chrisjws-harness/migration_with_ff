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

scrambled_content = """
[���������U��������������{�����������������������;���������������h������������:���������������������%����������������������(�����������������������������������������������������������������������������������������������������������������������������������k�������������������������
������������������������������������������������������������������������������������������������|���f���f���f���u���f���f���f���f���f���f���f���f���f���f���f���f���f���f�������f���f���f���f���f���f���f���f���f���f���f���f���f���E���f���f���p���f���f���f���f��
AA
  h
AG
  KA4,����^B�E�A �D(�G0A(D ABLd���`B�B�B �A(�D0�k
(A BBC
      {
(A EEH
      �� ����B�E�B �B(�A0�D8�G��Q�J�I�E�B�I�^
8A0A(B BBA
          `
�E
  ��E�Y�A�s
�E
  v�Y�E�B�I�N
�B
  (\8����B�E�G�Q
DK
  L������B�E�I �E(�D0�A8�G��
8D0A(B BBA
          �L����������`�
                        ����B�B�E �B(�A0�A8�G`�hCpZhA`whFpFhA`L
8D0A(B BBD
          \H���zDPp
A
 x����yM�`
A
 H�
   ����B�E�E �D(�A0�i
(D BBD
      Q(A BB\�P����F�B�B �B(�A0�A8�G��
�P�f
    R
8A0A(B BBE
          D��������������������ab�anbsbv#bE-bT7bA@b~���Eb}���F
$\���o��	�
�
���o���o�����o
         ���o@�@ P ` p � � � � � � � � !! !0!@!P!`!p!�!�!�!�!�!�!�!�!"" "0"@"P"`"p"�"�"�"�"�"�"�"�"## #0#@#P
         
"""

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
            if title == "Add feature flags to JavaScript app":
                content = scrambled_content
            else:
                content = "\n".join([line.strip() for line in f1])
            cursor.execute("INSERT INTO %s (title, content) VALUES ('CLOUD! %s', '%s')" % (table_name, title, content.replace("'", "")))

conn.commit()

cursor.close()
conn.close()

print("Data loaded into database...")
print("Done")
