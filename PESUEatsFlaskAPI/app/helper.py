import psycopg2
from psycopg2.extras import RealDictCursor
import os
import configparser

from flask import request, jsonify
from functools import wraps
import jwt


class AppConfig:
    """
    class containing the config state by reading the config.ini file
    """
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')


appconfig = AppConfig()

def get_cust_user():
    return appconfig.config['POSTGRES']['cust_user']

def get_pg_conn(*, dbname=None, user=None, host=None):
    if dbname is None:
        dbname = appconfig.config['POSTGRES']['dbname']
    if user is None:
        user = appconfig.config['POSTGRES']['default_user']
    if host is None:
        host = appconfig.config['POSTGRES']['host']

    con = psycopg2.connect(dbname=dbname, user=user, host=host)
    return con

def is_init():
    return appconfig.config['APP_CONFIG']['init']


def token_required(f):
    """
    Use this decorator on route endpoints to ensure that token verification
    is performed
    """
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, os.environ['SECRET_KEY'], algorithms="HS256")
            con = get_pg_conn()
            cur = con.cursor(cursor_factory=RealDictCursor)

            public_id = data['public_id']
        
            query = f"""SELECT * FROM app_users 
            WHERE public_id='{public_id}';
            """
            cur.execute(query)
            current_user = cur.fetchone()

        except:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)
    return decorator