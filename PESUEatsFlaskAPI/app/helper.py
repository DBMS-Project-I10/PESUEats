import psycopg2
from psycopg2.extras import RealDictCursor
import os
import configparser

from flask import request, jsonify, Response, json
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

def get_pg_conn(*, dbname=None, user=None, host=None, password=None):
    if dbname is None:
        dbname = appconfig.config['POSTGRES']['dbname']
    if user is None:
        user = appconfig.config['POSTGRES']['default_user']
    if host is None:
        host = appconfig.config['POSTGRES']['host']
    if password is None:
        try:
            password = appconfig.config['POSTGRES']['password']
        except:
            password=''
    con = psycopg2.connect(dbname=dbname, user=user, host=host, password=password)
    return con

def is_init():
    return appconfig.config['APP_CONFIG']['init']

def validate_dict(d):
    """
    Checks if any of the json fields is empty
    """
    for k in d:
        if d[k] == '':
            raise ValueError("Json is invalid (empty strings).")
    

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
            response = Response(
                response=json.dumps({
                    "message": "A valid token is missing.",
                }), 
                content_type='application/json',
                status=400
            )
            return response

        try:
            data = jwt.decode(token, os.environ['SECRET_KEY'], algorithms="HS256")
            con = get_pg_conn()
            cur = con.cursor(cursor_factory=RealDictCursor)

            public_id = data['public_id']
        
            query = f"""SELECT username, roles FROM app_users 
            WHERE public_id='{public_id}';
            """
            cur.execute(query)
            current_user = dict(cur.fetchone())
            
            if current_user['roles'] == 'customer':
                query = f"""SELECT custid FROM customer 
                WHERE custemail='{current_user['username']}';
                """
                cur.execute(query)
                custid = dict(cur.fetchone())['custid']

                current_user['custid'] = custid
                
            elif current_user['roles'] == 'restaurant':
                query = f"""SELECT rid FROM restaurant 
                WHERE remail='{current_user['username']}';
                """
                cur.execute(query)
                custid = dict(cur.fetchone())['rid']

                current_user['rid'] = custid
                
            elif current_user['roles'] == 'da':
                query = f"""SELECT daid FROM da 
                WHERE daemail='{current_user['username']}';
                """
                cur.execute(query)
                custid = dict(cur.fetchone())['daid']

                current_user['daid'] = custid
                

            cur.close()
            con.close()

        except:
            response = Response(
                response=json.dumps({
                    "message": "Token invalid.",
                }), 
                content_type='application/json',
                status=400
            )
            return response

        return f(current_user, *args, **kwargs)
    return decorator