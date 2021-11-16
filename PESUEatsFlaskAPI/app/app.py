from typing import ForwardRef
from flask import Flask, helpers, request, Response, jsonify, json
from flask.wrappers import Request
import psycopg2
from psycopg2.extras import RealDictCursor, wait_select
# import json


DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/')
    def hello():
        return 'Welcome to PESU Eats API!'

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
        
        response = app.response_class(
            response=json.dumps(items, indent=2),
            mimetype='application/json'
        )
        return response

    @app.route('/menuitems')
    def get_menuitems():
        """
        /menuitems
        /menuitems?rid={}
        """
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

        response = app.response_class(
            response=json.dumps(items, indent=2),
            mimetype='application/json'
        )
        return response
        return json.dumps(items, indent=2)


    @app.route('/menuitemincarts')
    def get_menuitemincarts():
        """
        /menuitemincarts

        /menuitemincarts?cartid=<cartid>
        """
        con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
        cur = con.cursor(cursor_factory=RealDictCursor)

        cartid = request.args.get('cartid')
        if cartid is None:
            cur.execute("SELECT * FROM MENU_ITEM_IN_CART;")
        
        else:
            cur.execute(f"SELECT * FROM MENU_ITEM_IN_CART WHERE MICartId = {cartid};")
        
        items = cur.fetchall()
        cur.close()
        con.close()

        response = app.response_class(
            response=json.dumps(items, indent=2),
            mimetype='application/json'
        )
        return response
        return json.dumps(items, indent=2)


    @app.route('/customer')
    def get_customer():
        """
        /customer

        /customer?cid=<cid>

        /customer?cname=<cname>
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

        response = app.response_class(
            response=json.dumps(items, indent=2),
            mimetype='application/json'
        )
        return response

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

        response = app.response_class(
            response=json.dumps(items, indent=2),
            mimetype='application/json'
        )
        return response

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

        response = app.response_class(
            response=json.dumps(items, indent=2),
            mimetype='application/json'
        )
        return response

        return json.dumps(items, indent=2)

    # @app.route('/resetdb')
    # def resetdb():
    #     """
    #     /resetdb
    #     """
    #     con = psycopg2.connect(dbname='pesu_eats', user='postgres', host='localhost')
    #     cur = con.cursor(cursor_factory=RealDictCursor)
    #     cur.execute("SELECT * FROM ORDER_TRANSACTION;")
    #     items = cur.fetchall()
    #     cur.close()
    #     con.close()

    #     response = app.response_class(
    #         response=json.dumps(items, indent=2),
    #         mimetype='application/json'
    #     )
    #     return response

        return json.dumps(items, indent=2)


    @app.route('/deliveryagent')
    def get_da():
        """
        /deliveryagent
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

        response = app.response_class(
            response=json.dumps(items, indent=2),
            mimetype='application/json'
        )
        return response
        return json.dumps(items, indent=2)

    return app

