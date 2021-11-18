from flask import Flask
import psycopg2

from app.helper import get_pg_conn


from routes import cust_bp

from routes.routes import api_bp


DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(api_bp)
    app.register_blueprint(cust_bp)
    return app

