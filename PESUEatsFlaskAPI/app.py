from typing import ForwardRef
from flask import Flask, helpers, request
from flask.wrappers import Request
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
    """
    /restaurants
    """
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM RESTAURANT;")
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)

@app.route('/menuitems')
def get_allmenuitems():
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)

    if request.args == None:
        cur.execute("SELECT * FROM MENU_ITEM;")
        items = cur.fetchall()
        cur.close()
        con.close()
        return json.dumps(items, indent=2)
    
    else:
        print(request.args)
        return json.dumps(request.args)


@app.route('/menuitemincarts')
def get_menuitemincarts():
    """
    /menuitemincarts
    """
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM MENU_ITEM_IN_CART;")
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)

@app.route('/customers')
def get_customers():
    """
    /customers
    """
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM CUSTOMER;")
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)

@app.route('/foodorders')
def get_foodorders():
    """
    /foodorders
    """
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM FOOD_ORDER;")
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)

@app.route('/ordertransactions')
def get_ordertransactions():
    """
    /ordertransactions
    """
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM ORDER_TRANSACTION;")
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)
