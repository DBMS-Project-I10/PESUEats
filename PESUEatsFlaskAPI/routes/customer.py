"""
Endpoints from a customer's pov
"""

import os
import datetime
import uuid
import jwt

from psycopg2.extras import RealDictCursor
from flask import (
    Blueprint, 
    request, 
    json, 
    Response, 
    jsonify
)

from app.helper import get_pg_conn, get_cust_user, token_required, validate_dict

#  url_prefix='/api'

cust_bp = Blueprint('customer', __name__)



@cust_bp.route('/signup/customer', methods=['POST'])
def signup():
    """
    Sign up/register a new customer
    """
    user_details = request.json
    public_id = str(uuid.uuid4())

    con = None
    cur = None

    try:

        # Check if necessary fields in post request

        required_fields = {'email', 'phone', 'name', 'password'}

        if not user_details or not (required_fields <= user_details.keys()):
            response = Response(
                response=json.dumps({
                    "message": "Missing a required parameter (email, phone, name or password)",
                }), 
                content_type='application/json',
                status=400
            )
            return response     

        # Checks if dict has eny empty strings
        validate_dict(dict((k, user_details[k]) for k in required_fields))

        # Make sure phone number can be converted to int
        phone = None
        try:
            phone = int(user_details['phone'])
        except Exception as e:
            response = Response(
                response=json.dumps({
                    "message": "Phone number not a valid phone number",
                }), 
                content_type='application/json',
                status=400
            )
            return response

        # Check if email already registered (we will use 
        # only email and not phone number) for simplicity
        con = get_pg_conn()
        cur = con.cursor(cursor_factory=RealDictCursor)

        email = user_details['email']
        # Check if user already exists
        query = f"""SELECT username FROM app_users 
            WHERE username = '{email}' and roles = 'customer';
        """
        cur.execute(query)
        
        if cur.fetchone() is None:
            if 'addr' in user_details.keys():
                addr = user_details['addr']
            else:
                addr = 'null'

            # First create a wallet entry
            query = f"""INSERT INTO WALLET VALUES (
                default, 0) RETURNING WID
            ;"""
            cur.execute(query)
            wid = cur.fetchone()['wid']
            
            # Insert new user into customer
            query = f"""INSERT INTO CUSTOMER VALUES (
                default, {wid}, null, '{phone}', 
                '{addr}', '{user_details['name']}', '{user_details['email']}'
            ) RETURNING custid;"""
            cur.execute(query)
            custid = cur.fetchone()['custid']
            
            # Insert into app_users
            query = f"""INSERT INTO APP_USERS VALUES (
                '{public_id}',
                '{email}',
                '{user_details['password']}',
                'customer'
            );"""
            cur.execute(query)

            # Commit changes
            con.commit()

            # Return the customer record inserted
            query = f"""SELECT CUSTPHONE, CUSTADDR, CUSTNAME, CUSTEMAIL FROM CUSTOMER 
                WHERE CUSTEMAIL = '{user_details['email']}';
            """
            cur.execute(query)        
            item = cur.fetchone()
            response = Response(
                response=json.dumps(item, indent=2),
                mimetype='application/json',
                status=200
            )

        else:
            response = Response(
                response=json.dumps({
                    "message": "User already exists. Please sign in.",
                }), 
                content_type='application/json',
                status=400
            )

    except Exception as e:
        response = Response(
            response=json.dumps({
                "message": "Error in request body.",
            }), 
            content_type='application/json',
            status=400
        )
        print(e)

    if cur is not None:
        cur.close()
    if con is not None:
        con.close()
    return response


@cust_bp.route('/addtocart', methods=["POST"])
@token_required
def addtocart(current_cust):
    """
    Add an item to the customer's cart
    """
    reqbody = request.json
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    custid = current_cust['custid']

    if 'itemid' not in reqbody.keys():
        response = Response(
            response=json.dumps({"message": "ItemId not present"}),
            mimetype='application/json',
            status=400
        )
        return response

    try:

        # Creating new cart if not present
        if 'cartid' not in reqbody.keys():
            cur.execute(f'''update cart set CartStatus = 'INACTIVE' where cartcustid = {custid};''')
            cur.execute(f'''insert into cart values (default, {custid}, 'ACTIVE', 0, 0, 25.0) returning cartid''')
            cartid = cur.fetchone()['cartid']
            con.commit() 
        else:
            cartid = reqbody["cartid"] 
        
        if 'quantity' in reqbody.keys():
            quantity = reqbody['quantity']
        else:
            quantity = 1

        #TODO : Figure out how to validate all items being added to cart are from the same restaurant (Might use Triggers and Functions)

        cur.execute(f'insert into menu_item_in_cart values ({reqbody["itemid"]}, {cartid}, {custid}, {quantity});')
        # When menu item is added into cart, triggers and fucntions defined in create.sql automatically update cart value and tax amounts 

        
        con.commit() 
        
        response = Response(
                response=json.dumps({"message": "Successfully added to cart", "cartid": cartid}),
                mimetype='application/json',
                status=200
            )
    except:
        response = Response(
            response=json.dumps({"message": "Error in requiest body."}),
            mimetype='application/json',
            status=400
        )
    if cur is not None:
        cur.close()
    if con is not None:
        con.close()

    return response

@cust_bp.route('/removefromcart', methods=["POST"])
@token_required
def removefromcart(current_cust):
    reqbody = request.json 
    con = get_pg_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)

    custid = current_cust['custid']

    if 'itemid' not in reqbody.keys() or 'cartid' not in reqbody.keys():
        response = Response(
            response=json.dumps({"message": "ItemId or CartId not present"}),
            mimetype='application/json',
            status=400
        )
        return response

    cur.execute(f'delete from menu_item_in_cart where miid = {reqbody["itemid"]} and micartid = {reqbody["cartid"]} and micartcustid = {custid};')
    # When menu item is added into cart, triggers and fucntions defined in create.sql automatically update cart value and tax amounts 
    con.commit() 

    cur.close()
    con.close()
    
    response = Response(
            response=json.dumps({"message": "Successfully removed from cart"}),
            mimetype='application/json',
            status=200
        )
    return response

@cust_bp.route('/showcart')
@token_required
def showcart(current_cust):
    """
    Show all items in a cart
    """
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)

    custid = current_cust['custid']
    # custid = request.args.get('custid')
    cartid = request.args.get('cartid')

    if cartid is None or custid is None:
        response = Response(
            response=json.dumps({"message": "CustId or CartId not present"}),
            mimetype='application/json',
            status=400
        )
        cur.close()
        con.close()
        return response
        
    
    cur.execute(f'SELECT Iid, Iname, Iprice, MIQuantity FROM MENU_ITEM m, MENU_ITEM_IN_CART mc WHERE m.Iid = mc.MIid AND mc.MICartId = {cartid};')
    res = cur.fetchall() 
    response = Response(
        response=json.dumps(res),
        mimetype='application/json',
        status=200
    )

    cur.close()
    con.close()

    return response
  

@cust_bp.route('/placeorder', methods=["POST"])
@token_required
def placeorder(current_cust):
    """
    Place an order
    """
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)

    reqbody = request.json 

    # custid = reqbody['custid']
    custid = current_cust['custid']
    cartid = reqbody['cartid']

    # custid = request.args.get('custid')
    # cartid = request.args.get('cartid')

    if cartid is None or custid is None:
        response = Response(
            response=json.dumps({"message": "CustId and CartId not present"}),
            mimetype='application/json',
            status=400
        )
        cur.close() 
        con.close()
        return response
        
    if cartid is None:
        cartid = cur.execute(f'SELECT cartid FROM CART WHERE cartcustid = {custid} and cartstatus = "ACTIVE";')

    #Get Restaurant Id
    cur.execute(f'SELECT IinMenuRid from MENU_ITEM_IN_CART mc, MENU_ITEM m where micartid = {cartid} and micartcustid = {custid} and mc.miid = m.iid;')
    rid = cur.fetchone()['iinmenurid']

    # Find free DAs 
    cur.execute(f'''SELECT DISTINCT DAId from DELIVERY_AGENT EXCEPT SELECT DISTINCT ODAId FROM FOOD_ORDER WHERE Ostatus != 'DELIVERED'; ''')
    #Pick the first free DA
    daid = cur.fetchone()['daid']

    try:
        cur.execute(f'''insert into food_order values (default, {rid}, {daid}, {cartid}, {custid}, NULL, 'PLACED', NOW()) returning oid;''')
    except Exception:
        response = Response(
            response=json.dumps({"message": "KeyError. The Cartid and Custid is already present"}),
            mimetype='application/json',
            status=400
        )
        return response

    oid = cur.fetchone()['oid']
    cur.execute(f'''update cart set cartstatus = 'INACTIVE' where cartid = {cartid} and cartcustid = {custid};''')
    con.commit() 

    cur.close() 
    con.close() 

    response = Response(
            response=json.dumps({"message": "Successfully placed order", "oid": oid}),
            mimetype='application/json',
            status=200
    )
    return response


@cust_bp.route('/restaurants')
@token_required
def get_restaurants(current_cust):
    """
    /restaurants
    """
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM RESTAURANT;")
    items = cur.fetchall()
    cur.close()
    con.close()
    
    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response

@cust_bp.route('/menuitems')
@token_required
def get_menuitems(current_cust):
    """
    /menuitems
    /menuitems?rid={}
    """
    con = get_pg_conn(user=get_cust_user())
    cur = con.cursor(cursor_factory=RealDictCursor)

    rid = request.args.get('rid')

    if rid is None:
        cur.execute("SELECT * FROM MENU_ITEM;")
    
    else:
        cur.execute(f"SELECT * FROM MENU_ITEM WHERE IinMenuRid = {rid};")
    
    items = cur.fetchall()
    cur.close()
    con.close()

    response = Response(
        response=json.dumps(items, indent=2),
        mimetype='application/json'
    )
    return response
    return json.dumps(items, indent=2)

# @cust_bp.route('/orders/customer/current', methods=["GET"])
# def getcurrentorders():
#     con = get_pg_conn(user=get_cust_user())
#     cur = con.cursor(cursor_factory=RealDictCursor)

#     custid = request.args.get('custid')

#     cur.execute(f'''select * from food_order where otocartcustid = {custid} and ostatus != "DELIVERED";''')
#     items = cur.fetchall() 
#     cur.close() 
#     con.close() 

#     response = Response(
#         response=json.dumps(items, indent=2),
#         mimetype='application/json'
#     )
#     return response

# @cust_bp.route('/orders/customer/history', methods=["GET"])
# def getprevorders():
#     con = get_pg_conn(user=get_cust_user())
#     cur = con.cursor(cursor_factory=RealDictCursor)

#     custid = request.args.get('custid')

#     cur.execute(f'''select * from food_order where otocartcustid = {custid} and ostatus = "DELIVERED";''')
#     items = cur.fetchall() 
#     cur.close() 
#     con.close() 

#     response = Response(
#         response=json.dumps(items, indent=2),
#         mimetype='application/json'
#     )
#     return response
    