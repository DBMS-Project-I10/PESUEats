"""

"""

from psycopg2.extras import RealDictCursor
from flask import Blueprint, request, json, Response

from app.helper import get_pg_conn

#  url_prefix='/api'

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def hello():
    return 'Welcome to PESU Eats API!'


@api_bp.route('/cartinfo')
def get_cart_info():
    """
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    cartid = request.args.get('cartid')

    if cartid is None:
        cur.execute("SELECT * FROM CART;")
    
    else:
        cur.execute(f"SELECT * FROM CART WHERE CartId = {cartid};")
    
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response
    return json.dumps(items, indent=2)


@api_bp.route('/customer')
def get_customer():
    """
    /customer

    /customer?cid=<cid>

    /customer?cname=<cname>
    """
    con = get_pg_conn()
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

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response

    return json.dumps(items, indent=2)
    

@api_bp.route('/foodorders')
def get_foodorders():
    """
    /foodorders
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM FOOD_ORDER;")
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response


@api_bp.route('/ordertransactions')
def get_ordertransactions():
    """
    /ordertransactions
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM ORDER_TRANSACTION;")
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response


@api_bp.route('/deliveryagent')
def get_da():
    """
    /deliveryagent
    """
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    daid = request.args.get('daid')
    daname = request.args.get('daname')

    if daid is None and daname is None:
        cur.execute("SELECT * FROM DA;")
    
    elif daname is None:
        cur.execute(f"SELECT * FROM DA WHERE CustId = {daid};")
    
    else:
        cur.execute(f"SELECT * FROM DA WHERE CustName = '{daname}';")
    
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response


    
