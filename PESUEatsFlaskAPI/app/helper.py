from flask import request, jsonify
from functools import wraps
import jwt


import psycopg2
import configparser

class AppConfig:
    """
    class containing the config state by reading the config.ini file
    """
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

appconfig = AppConfig()

def get_pg_conn(*, dbname=None, user=None, host=None):
    if dbname is None:
        dbname = appconfig.config['POSTGRES']['dbname']
    if user is None:
        user = appconfig.config['POSTGRES']['user']
    if host is None:
        host = appconfig.config['POSTGRES']['host']

    con = psycopg2.connect(dbname=dbname, user=user, host=host)
    return con


# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):

#         token = None

#         if 'x-access-tokens' in request.headers:
#             token = request.headers['x-access-tokens']

#         if not token:
#             return jsonify({'message': 'a valid token is missing'})

#         try:
#             data = jwt.decode(token, app.config[SECRET_KEY])
#             current_user = Users.query.filter_by(public_id=data['public_id']).first()
#         except:
#             return jsonify({'message': 'token is invalid'})

#             return f(current_user, *args, **kwargs)
#     return decorator