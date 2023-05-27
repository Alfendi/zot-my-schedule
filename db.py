import config
import os
import pymysql
# from flask import jsonify

db_user = os.environ.get(config.DB_USER)
db_password = os.environ.get(config.DB_PASSWORD)
db_name = os.environ.get(config.DB_NAME)
db_connection_name = os.environ.get(config.DB_CONNECTION_NAME)


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                   unix_socket=unix_socket, db=db_name,
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
    except pymysql.MySQLError as e:
        print(e)

    return conn
