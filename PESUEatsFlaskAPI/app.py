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
def get_menuitems():
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)

    rid = request.args.get('rid')

    if rid is None:
        cur.execute("SELECT * FROM MENU_ITEM;")
    
    else:
        cur.execute(f"SELECT * FROM MENU_ITEM WHERE IinMenuRid = {rid};")
    
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)


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


@app.route('/customer')
def get_customer():
    """
    /ordertransactions
    """
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)

    cid = request.args.get('cid')
    cname = request.args.get('cname')

    if cid is None and cname is None:
        cur.execute("SELECT * FROM CUSTOMER;")
    
    elif cname is None:
        cur.execute(f"SELECT * FROM CUSTOMER WHERE CustId = {cid};")
    
    else:
        cur.execute(f"SELECT * FROM CUSTOMER WHERE CustName = '{cname}';")
    
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)

@app.route('/deliveryagent')
def get_da():
    """
    /ordertransactions
    """
    con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    cur = con.cursor(cursor_factory=RealDictCursor)

    daid = request.args.get('daid')
    daname = request.args.get('daname')

    if daid is None and daname is None:
        cur.execute("SELECT * FROM DELIVERY_AGENT;")
    
    elif daname is None:
        cur.execute(f"SELECT * FROM DELIVERY_AGENT WHERE CustId = {daid};")
    
    else:
        cur.execute(f"SELECT * FROM DELIVERY_AGENT WHERE CustName = '{daname}';")
    
    items = cur.fetchall()
    cur.close()
    con.close()
    return json.dumps(items, indent=2)


