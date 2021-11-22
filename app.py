import json
from logging import currentframe
import os
from flask import Flask, jsonify
from flask_cors import CORS
import redis
from db import db
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
cors = CORS(app, resources={f"*": {"origins": "*"}})

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', '6379')
red = redis.Redis(host=redis_host, port=redis_port)

local_db = os.environ.get('LOCAL_DB', 'false') in ['True', 'true']
db_host = os.environ.get('DB_HOST', 'localhost')
db_user = os.environ.get('DB_USER', 'root')
db_passwd = os.environ.get('DB_PASSWORD', 'myAwesomePassword')
db_name = os.environ.get('DATABASE', 'mydb')

init_db = os.environ.get('INIT_DB', 'true') in ['True', 'true']

conn = None


class DbInitHelper:

    def __init__(self):
        self.is_data_set = False
        self.create_db()
        self.conn = mysql.connector.connect(host=db_host, user=db_user, passwd=db_passwd, database=db_name)
        print(f'Successfully created DB connection for database <{db_name}>.')
        self.create_table()

    def create_db(self):
        try:
            conn = mysql.connector.connect(host=db_host, user=db_user, passwd=db_passwd)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            conn.close()

            print(f'Successfully created database <{db_name}>, if not exists.')
            self.is_data_set = True
        except mysql.connector.Error as err:
            app.logger.info("Failed creating database: {}".format(err))
            print("Failed creating database: {}".format(err))

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            print("Creating table users")
            cursor.execute("""
                CREATE TABLE `users` (
                  `id` int NOT NULL,
                  `username` varchar(50) NOT NULL,
                  `name` varchar(50) NOT NULL,
                  `bio` varchar(50) NOT NULL,
                  PRIMARY KEY (`id`)
                );
            """)

            cursor.execute("""
                insert into `users`(`id`,`username`,`name`,`bio`)
                values (1,'marceline','Marceline Abadeer','1000 year old vampire queen, musician');
            """)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(f"Table <users> already exists.")
            else:
                print(err.msg)
        else:
            print(f'Successfully inserted data into table <users>.')

    def get_connection(self):
        return self.conn


def get_from_db(table):
    if local_db:
        return db.get(table)
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()
    except Exception as error:
        return "SQL error running: " + str(error)
 

@app.route('/api/users', methods=['GET'], strict_slashes=False)
def users():
    body = {}
    key = "users"
    try:
        value = red.get(key)
        if not value:
            data = get_from_db(key)
            keys = ['id', 'username', 'name', 'bio']
            obj = dict(zip(keys, data[0]))
            red.set(key, str(json.dumps(obj)))

            body['source'] = 'database'
            body['data'] = obj
        else:
            body['source'] = 'redis'
            body['data'] = json.loads(value.decode('ascii'))

        print("Body:")
        print(body)
        return jsonify(body), 200
    except Exception as error: 
        print(error)
        body['data'] = error
        return str(error), 200

@app.route('/api/users/clear-cache', methods=['GET'], strict_slashes=False)
def clear_cache():
    red.delete("users")

    return "cleared users", 200
    
@app.route('/api/users/health', methods=['GET'], strict_slashes=False)
def health():
    return "", 200


if init_db:
    conn = DbInitHelper().get_connection()
    if conn.is_connected():
        print('Successfully completed DB init.')
        print(get_from_db('users'))


if __name__ == '__main__':
    app.run()
