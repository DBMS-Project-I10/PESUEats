from typing import ForwardRef
from flask import Flask, helpers
import psycopg2
from psycopg2.extras import RealDictCursor, wait_select
import json

app = Flask(__name__)

DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/restaurants')
def get_restaurants():
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM RESTAURANT;")
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)

@app.route('/')
def get_menuitemincarts():
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM MENU_ITEM_IN_CART;")
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)
