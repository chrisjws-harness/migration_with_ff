# import time
import psycopg2
from psycopg2.extras import DictCursor

from flask import Flask, render_template
import sqlite3
from werkzeug.exceptions import abort
from featureflags.client import CfClient
from featureflags.evaluations.auth_target import Target
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

api_key = config.get('feature_flags', 'key')
cf = CfClient(api_key)
target = Target(identifier="user1", name="user1")

app = Flask(__name__)


def get_db_connection_cloud():
    conn = psycopg2.connect(**params)
    return conn


def get_post_cloud(post_id):
    conn = get_db_connection_cloud()
    cur = conn.cursor()
    cur.execute("SELECT * FROM %s" % table_name)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if post is None:
        abort(404)
    return post


def get_posts_cloud():
    conn = get_db_connection_cloud()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM %s" % table_name)
    rows = cur.fetchall()
    results = []
    for row in rows:
        result = {}
        for key, value in row.items():
            result[key] = value
        results.append(result)
    cur.close()
    conn.close()
    return results


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return posts


@app.route('/')
def index():
    rds = cf.bool_variation("migrate_to_rds", target, False)
    if rds:
        posts = get_posts_cloud()
    else:
        posts = get_posts()

    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
